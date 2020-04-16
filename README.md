# ECHO BOT
Barebones echo agent that repeats what is said or written as an input to start with Embodied Conversational Agents Projects with Smartbody behavior realizer.


## Getting Started
The project is written on Python and works on Python >= 3.6

This project uses Smartbody character animation system as a character animation platform in Windows. Download Smartbody from: http://smartbody.ict.usc.edu/
I have noticed USC does not directly support Smartbody anymore but it is still available within the Virtual Human Toolkit: https://vhtoolkit.ict.usc.edu/download/

A version of this project that uses Unity instead of Smartbody is under development at iVizLab, Simon Fraser University. We will soon migrate to this version and ECHO_BOT currently supports both Smartbody and Unity integration.

You will need ActiveMQ running in your computer. Follow instructions from : https://activemq.apache.org/getting-started
You might want to run the broker as a service in Windows that automatically runs at start-up, for ease of use.

This project is using Google Speech-to-Text API. You should setup an account for google-cloud-speech and set your credentials following this documentation:
https://cloud.google.com/speech-to-text/docs/libraries

I have used Sphinx formerly but did not have time to train my own model and eventually decided to use the cloud-based solution. If you want to use your own recognizer, you can do so by creating a new recognizer instance similar to the Google implementation.


## Installing

We recommend creating a virtual environment with Python >= 3.6, clone the project and use requirements.txt to prepare your environment.

```
pip install -r requirements.txt
```


## Running ECHO BOT
1. Start Smartbody and make sure ActiveMQ is running
2. Load Character using one of the files in https://github.com/onyalcin/echo_bot_/tree/master/Smartbody_files, the config files currently uses Matt. Wait until you see the character in Smartbody.
3. Run TTSRelay within Smartbody
4. In your virtualenv, run:
```
python -m dialogue_system
```
5. Use push-to-talk to speak with the avatar or type to start written conversation.

