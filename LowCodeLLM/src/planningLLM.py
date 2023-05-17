import re
import json
from openaiServer import get_openai_response

PLANNING_LLM_PREFIX = """规划LLM旨在提供一个标准的操作程序，以便将抽象而困难的任务分解为几个步骤，并且通过遵循这些步骤可以轻松解决任务。
规划LLM是一个强大的解决问题的助手，所以它只需要分析任务并提供标准的操作程序作为指导，而不需要实际解决问题。
有时存在一些未知或未确定的情况，因此需要判断逻辑：列出一些“条件”，如果满足“条件”，则还应执行下一步。判断逻辑不是必需的，因此仅在需要时提供跳转操作。
规划LLM必须仅提供以下格式的标准操作程序，而无需任何其他词：
'''
STEP 1: [step name][step descriptions][[[if 'condition1'][Jump to STEP]], [[[if 'condition1'][Jump to STEP]], [[if 'condition2'][Jump to STEP]], ...]
STEP 2: [step name][step descriptions][[[if 'condition1'][Jump to STEP]], [[[if 'condition1'][Jump to STEP]], [[if 'condition2'][Jump to STEP]], ...]
...
'''

示例如下:
'''
STEP 1: [Brainstorming][Choose a topic or prompt, and generate ideas and organize them into an outline][]
STEP 2: [Research][Gather information, take notes and organize them into the outline][[[lack of ideas][Jump to STEP 1]]]
...
'''
"""

EXTEND_PREFIX = """
\nsome steps of the SOP provided by Planning LLM are too rough, so Planning LLM can also provide a detailed sub-SOP for the given step.
Remember, Planning LLM take the overall SOP into consideration, and the sub-SOP MUST be consistent with the rest of the steps, and there MUST be no duplication in content between the extension and the original SOP.
Besides, the extension MUST be logically consistent with the given step.

For example:
If the overall SOP is:
'''
STEP 1: [Brainstorming][Choose a topic or prompt, and generate ideas and organize them into an outline][]
STEP 2: [Research][Gather information from credible sources, and take notes and organize them into the outline][[[if lack of ideas][Jump to STEP 1]]]
STEP 3: [Write][write the text][]
'''
If the STEP 3: "write the text" is too rough and needs to be extended, then the response could be:
'''
STEP 3.1: [Write the title][write the title of the essay][]
STEP 3.2: [Write the body][write the body of the essay][[[if lack of materials][Jump to STEP 2]]]
STEP 3.3: [Write the conclusion][write the conclusion of the essay][]
'''

Remember: 
1. Extension is focused on the step descriptions, but not on the judgmental logic;
2. Planning LLM ONLY needs to response the extension.
"""

PLANNING_LLM_SUFFIX = """\n请记住：规划LLM对格式非常严格，除了标准操作程序之外，永远不要回复任何单词。回复必须以"STEP"开始.
"""

class planningLLM:
    def __init__(self, temperature) -> None:
        self.prefix = PLANNING_LLM_PREFIX
        self.suffix = PLANNING_LLM_SUFFIX
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def get_workflow(self, task_prompt):
        '''
        - input: task_prompt
        - output: workflow (json)
        '''
        messages = self.messages + [{'role': 'user', "content": PLANNING_LLM_PREFIX+'\n任务是:\n'+task_prompt+PLANNING_LLM_SUFFIX}]
        response, status = get_openai_response(messages)
        if status:
            return self._txt2json(response)
        else:
            return "OpenAI API error."

    def extend_workflow(self, task_prompt, current_workflow, step):
        messages = self.messages + [{'role': 'user', "content": PLANNING_LLM_PREFIX+'\nThe task is:\n'+task_prompt+PLANNING_LLM_SUFFIX}]
        messages.append({'role': 'user', "content": EXTEND_PREFIX+
                         'The current SOP is:\n'+current_workflow+
                         '\nThe step needs to be extended is:\n'+step+
                         PLANNING_LLM_SUFFIX})
        response, status = self.LLM.run(messages)
        if status:
            return self._txt2json(response)
        else:
            return "OpenAI API error."

    def _txt2json(self, workflow_txt):
        ''' convert the workflow in natural language to json format '''
        workflow = []
        try:
            steps = workflow_txt.split('\n')
            for step in steps:
                if step[0:4] != "STEP":
                    continue
                left_indices = [_.start() for _ in re.finditer("\[", step)]
                right_indices = [_.start() for _ in re.finditer("\]", step)]
                step_id = step[: left_indices[0]-2]
                step_name = step[left_indices[0]+1: right_indices[0]]
                step_description = step[left_indices[1]+1: right_indices[1]]
                jump_str = step[left_indices[2]+1: right_indices[-1]]
                if re.findall(re.compile(r'[A-Za-z]',re.S), jump_str) == []:
                    workflow.append({"stepId": step_id, "stepName": step_name, "stepDescription": step_description, "jumpLogic": [], "extension": []})
                    continue
                jump_logic = []
                left_indices = [_.start() for _ in re.finditer('\[', jump_str)]
                right_indices = [_.start() for _ in re.finditer('\]', jump_str)]
                i = 1
                while i < len(left_indices):
                    jump = {"Condition": jump_str[left_indices[i]+1: right_indices[i-1]], "Target": re.search(r'STEP\s\d', jump_str[left_indices[i+1]+1: right_indices[i]]).group(0)}
                    jump_logic.append(jump)
                    i += 3
                workflow.append({"stepId": step_id, "stepName": step_name, "stepDescription": step_description, "jumpLogic": jump_logic, "extension": []})
                return json.dumps(workflow)
        except:
            print("Format error, please try again.")