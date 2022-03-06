# QA challenge for Voicemod / 2022 /

## **Repository structure**

```
.
├── resources
│   ├── __init__.py
│   ├── lib_voicemoduat.py
│   ├── locators.py
│   └── variables.py
├── .gitignore
├── Dockerfile
├── README.md
├── results.zip                     (See more info below)
├── sonar-project.properties
└── VoicemodUAT.robot
```

- Robot test results available in results.zip
- Screenshots for each test case available in their respective folders
- We're excluding the downloaded VoicemodSetup_2.26.0.1.exe file
- Unzipped results.zip will look like:
```
├── results
    ├── log.html
    ├── output.xml
    ├── report.html
    ├── Test 1
    │   ├── screenshot-1.png
    │ [...]
    │   └── screenshot-n.png
  [...]
    └── Test 5
        ├── screenshot-1.png
      [...]
        └── screenshot-n.png
```

## **Usage (example instructions for Ubuntu 20.04)**

1. Build Docker image from Dockerfile
2. Execute robot command

### **1. Build Docker image from Dockerfile**

```bash
docker build -f ./Dockerfile -t voicemod_uat_docker .
```

### **2. Execute robot command**

- Loglevel can be adjusted to DEBUG level to get more verbose logs

```bash
export WORKSPACE="/opt/voicemod_uat" && \
docker run --rm -it --privileged \
--name voicemod_uat \
--network=host \
-w $WORKSPACE \
-v $(pwd):$WORKSPACE \
voicemod_uat_docker \
robot --outputdir $WORKSPACE/results \
--loglevel INFO \
--pythonpath ":.:resources:" ./VoicemodUAT.robot
```
