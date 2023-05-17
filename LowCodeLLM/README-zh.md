Low-code LLM

Low-code LLM 是一种新颖的人类-LLM 交互模式，让人类参与循环以实现更可控和稳定的响应。

请参阅我们的论文：Low-code LLM: Visual Programming over LLMs

未来，TaskMatrix.AI 可以通过更有效地分解任务，利用现有的基础模型和其他 AI 模型和系统的 API 来增强任务自动化，从而在数字和物理领域实现多样化的任务。低代码的人-LLM 交互模式可以增强用户在控制流程和表达偏好方面的体验。
Video Demo
Lowcode.mp4

（这是演示完整过程的概念视频演示）
Quick Start

请注意，由于时间关系，我们提供的代码只是low-code LLM交互代码的最小可行版本，即只展示Low-code LLM人-LLM交互的核心概念。我们欢迎任何有兴趣改进我们的前端界面的人。目前， OpenAI API 和 Azure OpenAI Service 均受支持。您需要提供调用这些 API 所需的信息。

# clone the repo
git clone https://github.com/microsoft/TaskMatrix.git

# go to directlory
cd LowCodeLLM

# build and run docker
docker build -t lowcode:latest .

# If OpenAI API is being used, it is only necessary to provide the API key.
docker run -p 8888:8888 --env OPENAIKEY={Your_Private_Openai_Key} lowcode:latest

# When using Azure OpenAI Service, it is advisable to store the necessary information in a configuration file for ease of access.
# Kindly duplicate the config.template file and name the copied file as config.ini. Then, fill out the necessary information in the config.ini file.
docker run -p 8888:8888 --env-file config.ini lowcode:latest

您现在可以通过访问演示页面来尝试
System Overview

overview

如上图所示，human-LLM交互可以通过以下方式完成：

    A Planning LLM that generates a highly structured workflow for complex tasks.
    为复杂任务生成高度结构化工作流的规划 LLM。
    Users editing the workflow with predefined low-code operations, which are all supported by clicking, dragging, or text editing.
    用户使用预定义的低代码操作编辑工作流，这些操作均通过单击、拖动或文本编辑来支持。
    An Executing LLM that generates responses with the reviewed workflow.
    一个正在执行的 LLM，它通过审查的工作流程生成响应。
    Users continuing to refine the workflow until satisfactory results are obtained.
    用户继续改进工作流程，直到获得满意的结果。

六种预定义的低代码操作

operations
Advantages

    可控生成。复杂的任务被分解为结构化的执行计划，并作为工作流呈现给用户。用户可以通过低代码操作来控制LLM的执行，以实现更可控的响应。按照定制的工作流程生成的响应将更符合用户的要求。
    友好互动。直观的工作流程使用户能够快速理解 LLM 的执行逻辑，通过图形用户界面的低代码操作使用户能够以用户友好的方式方便地修改工作流程。通过这种方式，可以减少耗时的提示工程，使用户能够有效地将他们的想法转化为详细的说明，从而获得高质量的结果。
    适用性广。所提出的框架可以应用于各个领域的广泛复杂任务，特别是在人类智慧或偏好不可或缺的情况下。

Acknowledgement

本文的一部分是通过与拟议的低代码 LLM 的交互协作制作的。该过程从 GPT-4 概述框架开始，随后作者用创新想法对其进行补充并改进工作流程的结构。最终，GPT-4 负责生成连贯且引人注目的文本。