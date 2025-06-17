# PFA - Personal Finance Assistant 

The Personal Finance Assistant or PFA is an AI agent that autonomously creates, manages, and rebalances a assets portfolio based on the user’s risk tolerance, investment goals, and market trends.

### To run locally:
```bash
uv venv
source .venv/bin/activate
uv sync
chainlit run app.py -w
```
#### Roadmap & Use Case: [DESCRIPTION.md](docs/DESCRIPTION.md)

#### Supported Financial Markets: [FINANCIAL MARKETS](docs/MARKETS.md)


### PFA Basic Agent Outline

``` 
├──1.RiskAssessmentAgent  
├
├──2.MarketAnalysisAgent  
├
├──3.RecommendationAgent → LLM-as-a-Judge(Validate)  
├
├──4.ComplianceGuardrail (Block unsafe actions)  
├
└──5.ExecutionAgent  

```

```

Frontend (UI/Form)
│
├── Collect User Data
│
└── Risk Assessment Agent
    ├── Rule-Based Scoring OR LLM Analysis
    ├── Guardrails (Safety Checks)
    └── Output Structured Risk Profile → Pass to Recommendation Agent
    
```

### Roadmap
- [x] User Information Process + Basic Operations on User Crypto Account
- [ ] For Further Phases see [docs](docs/DESCRIPTION.md)