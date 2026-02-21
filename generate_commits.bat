@echo off
echo Initializing Git repository...
git init

echo Commit 1: Project setup and Business Problem
git add docs\01_business_problem.md docs\02_project_scope.md docs\03_technical_approach.md docs\04_success_criteria.md
git commit -m "docs: define business problem and project scope"

echo Commit 2: Data Acquisition Script
git add src\01_data_acquisition.py
git commit -m "feat(data): create script to download UCI retail dataset"

echo Commit 3: Initial Data Exploration
git add notebooks\01_initial_data_exploration.ipynb
git commit -m "analysis: perform initial EDA on raw retail data"

echo Commit 4: Data Quality Summary JSON
git add data\raw\data_quality_summary.json
git commit -m "chore(data): save raw data quality profile metrics"

echo Commit 5: Data Cleaning Strategy Docs
git add docs\05_data_cleaning_strategy.md docs\06_data_dictionary.md
git commit -m "docs: formalize data cleaning strategy and raw dictionary"

echo Commit 6: Data Cleaning Script Implementation
git add src\02_data_cleaning.py
git commit -m "feat(data): implement 9-step cleaning pipeline"

echo Commit 7: Data Validation and Reporting
git add notebooks\02_data_validation.ipynb data\processed\cleaning_statistics.json data\processed\validation_report.json
git commit -m "test(data): validate assertions on cleaned datasets"

echo Commit 8: Cleaning Report Documentation
git add docs\07_data_cleaning_report.md
git commit -m "docs: summarize data cleaning execution and challenges"

echo Commit 9: Churn Definition logic
git add docs\08_churn_definition.md
git commit -m "docs: define dynamic 90-day churn observation logic"

echo Commit 10: Feature Engineering implementation
git add src\03_feature_engineering.py
git commit -m "feat(features): engineer RFM, temporal, and product diversity metrics"

echo Commit 11: Feature Dictionary and metadata
git add docs\09_feature_dictionary.md data\processed\feature_info.json
git commit -m "docs: document engineered behavioral feature set"

echo Commit 12: Feature EDA Notebook
git add notebooks\03_feature_eda.ipynb src\generate_eda_nb.py
git commit -m "analysis: generate visual distributions for churn features"

echo Commit 13: Feature Insights documentation
git add docs\10_eda_insights.md
git commit -m "docs: identify predictive factors from exploratory visualizations"

echo Commit 14: Model Preparation script
git add src\04_model_preparation.py
git commit -m "feat(model): create Train/Val/Test splitting and scaling pipeline"

echo Commit 15: Baseline Model implementations
git add notebooks\04_baseline_model.ipynb
git commit -m "feat(model): train baseline Logistic Regression on RFM data"

echo Commit 16: Advanced ML Models
git add notebooks\05_advanced_models.ipynb
git commit -m "feat(model): train XGBoost, Random Forest, and Decision Trees"

echo Commit 17: Model Selection Justification
git add docs\11_model_selection.md
git commit -m "docs: compare models and select XGBoost via ROC-AUC criteria"

echo Commit 18: Final Model Evaluation
git add notebooks\06_model_evaluation.ipynb
git commit -m "test(model): evaluate champion XGBoost against holdout set"

echo Commit 19: Cross Validation testing
git add notebooks\07_cross_validation.ipynb
git commit -m "test(model): perform 5-fold CV to verify model stability"

echo Commit 20: Business Impact calculations
git add docs\12_business_impact_analysis.md
git commit -m "docs: forecast financial ROI of predicted churn interventions"

echo Commit 21: Streamlit deployment scripts
git add app\predict.py app\streamlit_app.py
git commit -m "feat(ui): implement Streamlit dashboard and inference class"

echo Commit 22: Deployment guides and configs
git add deployment\deployment_guide.md Dockerfile docker-compose.yml requirements.txt
git commit -m "chore(deploy): add docker orchestration and requirements"

echo Commit 23: Final Technical documentation
git add docs\13_technical_documentation.md docs\14_self_assessment.md README.md submission.json .gitignore
git commit -m "docs: finalize README, technical architecture, and submission"

echo Commit 24: Generated artifacts
git add models\ presentation_content.md
git commit -m "chore(models): save serialized pipelines and presentation"

echo Commit 25: Adding all remaining project files
git add data\processed\* visualizations\*
git commit -m "chore: add all processed arrays and visual artifacts"

echo All commits generated successfully. You can now configure your remote and push using:
echo git remote add origin ^<YOUR_GITHUB_REPO_URL^>
echo git push -u origin master
