# ECHO BOT
Barebones echo agent that repeats what is said or written as an input to start with Embodied Conversational Agents Projects with Smartbody behavior realizer.


## Getting Started
The project is written on Python and works on Python >= 3.6

This project uses Smartbody character animation system as a character animation platform in Windows. Download Smartbody from: http://smartbody.ict.usc.edu/

A version of this project that uses Unity instead of Smartbody is under development at iVizLab, Simon Fraser University.

You will also need ActiveMQ running in your computer. Follow instructions from : https://activemq.apache.org/getting-started
You might want to run the broker as a service in Windows that automatically runs at start-up, for ease of use.

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

