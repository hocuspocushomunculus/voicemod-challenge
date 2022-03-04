# voicemod-challenge
QA challenge for Voicemod / 2022 /

# Repository structure
.
├── Dockerfile
├── notes.md
├── README.md
├── resources
│   └── variables.yaml
├── results
│   ├── geckodriver.log
│   ├── log.html
│   ├── output.xml
│   ├── report.html
│   ├── Test 1
│   │   ├── screenshot-1.png
│   │ [...]
│   │   └── screenshot-n.png
| [...]
│   ├── Test 5
│   │   ├── screenshot-1.png
│   │ [...]
│   │   └── screenshot-n.png
├── sonar-project.properties
└── VoicemodUAT.robot

# Build docker image
```bash
docker build -f ./Dockerfile -t voicemod_uat_docker .
```

# Run test suite
```bash
export WORKSPACE="/opt/voicemod_uat" && \
docker run --rm -it --privileged \
--name voicemod_uat \
--network=host \
-w $WORKSPACE \
-v $(pwd):$WORKSPACE \
voicemod_uat_docker \
robot --outputdir $WORKSPACE/results \
--loglevel DEBUG \
--pythonpath ":.:resources:" ./VoicemodUAT.robot
```

# Log files available in results/ folder for each test case
