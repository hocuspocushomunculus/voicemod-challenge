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
│   ├── selenium-screenshot-1.png
│ [...]
│   └── selenium-screenshot-n.png
└── VoicemodUAT.robot

# Build docker image
```bash
docker build -f ./Dockerfile -t voicemod_uat_docker .
```

# Run test suite
```bash
export WORKSPACE="/tmp/voicemod_uat" && \
docker run --rm -it --privileged \
--name voicemod_uat \
--network=host \
-w $WORKSPACE \
-v $(pwd):$WORKSPACE \
voicemod_uat_docker \
robot --outputdir $WORKSPACE/results ./VoicemodUAT.robot
```

# Log files available in reports/ folder
