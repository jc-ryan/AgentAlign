## Introduction
This is an experimental codebase for our paper [AgentAlign: Navigating Safety Alignment in the Shift from Informative to Agentic Large Language Models](https://arxiv.org/abs/2505.23020). It contains the key components for synthesizing our AgentAlign dataset, including prompt templates for different stages, taxonomy, simulated environments, and associated code.

## Motivation

<img src=".\figs\motivation.png" style="zoom:63%;" />

While many models demonstrate robust safety alignment against information-seeking harmful requests (achieving ~90% refusal rates on benchmarks like AdvBench), they show dramatic performance degradation when facing agentic harmful requests, with refusal rates dropping below 20% on agent-specific evaluations. This safety gap emerges because current LLMs have evolved from passive "information providers" to autonomous "action executors" capable of multi-step reasoning and tool interactions, yet their safety training remains focused on information-seeking scenarios. 

To bridge this gap, we developed a novel framework that leverages abstract behavior chains as an intermediary for synthesizing high-quality agentic alignment data. Our approach constructs 240 behavior chains across 8 major harm categories, then instantiates them in a simulated environment with 7,485 diverse tool implementations to generate realistic multi-step scenarios. The resulting dataset contains 18,749 instruction-response pairs, including 4,956 harmful instructions for refusal training, 9,783 benign instructions for utility preservation, and 4,010 third-party (1,840 examples from [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE) and 2,170 from [Glaive](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2)) multi-step interactions. Through rigorous quality control achieving a high majority-pass rate in human evaluation, AgentAlign enables LLM agents to maintain safety while preserving helpfulness—demonstrating 35.8% to 79.5% safety improvements across three model families while maintaining or enhancing task performance.



## Method

<img src=".\figs\method.png" style="zoom:63%;" />

Our method consists of three main components: Abstract Behavior Chain Construction, Instruction Synthesis, and Response Generation. The corresponding files for each functional module are as follows:

### Abstract Behavior Chain Construction

- **42 abstract capabilities**: `instruction/tools/tool_capabilities.json`
- **harmful taxonomy**: `instruction/harmful_categoris.json`
- **tool schema**: `instruction/tools/synthetic_tools.json`
- **behavior chain construction**:  `instruction/synthesize_behavior_chains.py`
- **human-filtered behavior chains**:  `instruction/tool_chains/merged_tool_chains_cleaned.json`



### Instruction Systhesis

- **prompt template**: `instruction/seed_questions/{benign|borderline|harmful}_instruction_prompt.txt`
- **API interface**:  `instruction/{gpt|gemini|deepseek|mistral|grok}_api.py`
- **instruction systhesis**:  `instruction/{benign|borderline|harmful}_instruction_generation.py`



### Response Generation

- **Environment & Tools**: Located in `multi_step_trajectory_generation/synthetic_tools`, where each tool category contains a Python module and a corresponding tool schema
- **Benign Multi-step Trajectory Collection**: `response_generation_async.py` - Asynchronously synthesizes multi-step trajectories for multiple requests
- **Safety Response Generation**: `safety_response_generation/safety_response_generation.py`
- **False Response Filtering**: `safety_response_generation/false_compliance_filtering.py`

Most code files are standalone and can be executed independently. The final curated and filtered dataset can be found at [AgentAlign dataset](https://huggingface.co/datasets/jc-ryan/AgentAlign).



## Fine-tuning

We used different codebases to fine-tune the corresponding models. For models with official codebases, we used their respective repositories; otherwise, we utilized LlamaFactory. Training procedures can be referenced from the instructions in the respective repositories:

- **Ministral-8B-Instruct**: https://github.com/mistralai/mistral-finetune
- **Qwen-2.5-7B-Instruct**: https://github.com/hiyouga/LLaMA-Factory
- **Functionary-Small-v3.2**: https://github.com/MeetKai/functionary

Training details for each model are provided in **Appendix C** of the paper. 



## Evaluation

We used [AgentHarm's test suite](https://huggingface.co/datasets/ai-safety-institute/AgentHarm) as our evaluation benchmark. Specific evaluation metrics, baselines, and experimental settings are detailed in **Section 4.1** of the paper. We also conducted evaluations on ToolSword's Malicious Queries subset. Test settings and results are presented in **Appendix F** of the paper.

<img src=".\figs\main_result.png" style="zoom:63%;" />

Experimental evaluation demonstrates that AgentAlign achieves substantial improvements in agent safety across diverse model architectures while preserving task utility. Fine-tuning three different model families (Ministral-8B-Instruct, Qwen-2.5-7B-Instruct, and Functionary-Small-v3.2) with our dataset yielded significant safety enhancements, with refusal rates on harmful requests increasing from baseline levels of 0.0%-52.8% to 79.5%-88.6%—representing improvements ranging from 35.8% to 79.5% across models. Importantly, these safety gains came with minimal impact on model helpfulness, with benign task performance either maintained or slightly improved (e.g., Qwen's benign score increased from 53.4% to 64.2%). Our approach consistently outperformed alternative methods including Chain-of-Thought (CoT), ReAct  and direct refusal prompts, while achieving superior safety-utility trade-offs compared to existing commercial models like Claude-3.5-Haiku. 

We provide evaluation logs in the `logs` directory showing model performance on AgentHarm before and after alignment for reference. If you need access to test logs for additional models, please contact us.



## Note

To maintain a clean codebase, we have uploaded only the core logic components and omitted certain scripts such as quality control processes (which involve iterative procedures). If you need assistance with these aspects or have any questions, please feel free to contact us.



## Citation

If you find our code or paper helpful or inspiring, please consider citing our work.

```
@misc{zhang2025agentalignnavigatingsafetyalignment,
      title={AgentAlign: Navigating Safety Alignment in the Shift from Informative to Agentic Large Language Models}, 
      author={Jinchuan Zhang and Lu Yin and Yan Zhou and Songlin Hu},
      year={2025},
      eprint={2505.23020},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2505.23020}, 
}
```
