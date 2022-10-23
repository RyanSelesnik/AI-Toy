# 2 October 

## Results
- Implemented real-time speech recognition using Wav2Vec
- Implemented response generation using DialoGPT
- Evaluated response generation algorithm with regards to latency, CPU usage, and memory occupancy.

## What Went Well
- We split up the weeks sprint into independent tasks which meant that we could work separately and in our own time, and our tasks were decoupled so that we weren't reliant on each other to finish their work before moving on.
- Used classes to integrate our individual tasks seamlessly
- Stand-ups were valuable because we didn't need to commit too much time to discussions and we were kept in the loop of each other's progress

## What Didn't Go Well
- Too many moving parts in the sprint
- The sprint goal wasn't actually directed at answering the investigation question - investigating and implementing a system that can be used in the production of a **low cost** device, using **low complexity** algorithms.
- We didn't refine the research question well enough, and further, we didn't use that to inform the tasks we needed to achieve in the sprint.
- Lost clarity on what we were trying to achieve so stand-ps, and individual tasks faded away
  
## Going forward into Sprint 2
- Try to define the research question more clearly
- Formalise the tasks 
- Use the research question to inform the formalised tasks
- Keep doing daily stand-ups with the following format
  1. What did you yesterday?
  2. What are you going to do today?
  3. What is blocking you?  

# 9 October

## Results
- Implemented a draft of the memory game "i went to the market and i bought..." since memory games are said to help with child development
- Implemented basic Rasa text-based chatbot
- Implemented a draft of the math game "fizz-buzz" since maths is said to help with child development

## What Went Well
- We had a more holistic overview of what we want to do  
- Tasks were well split between us so we had direction consistently and didn't need to rely on each other

## What Didn't Go Well
- Sprint goal was not well defined
- Did not touch all layers in the system 
- Did not measure anything 
- User can't interface with the system 

## Going Forward into Sprint 3
- Define a clearly acheivable sprint goal
- Touch front end of the system - user interface
- Touch backend of system - Speech to text, text to speech and Rasa 
- Evaluate system 
- Set new dealines for upcoming tasks i.e. Raspberry Pi, CV, presentable system 
- Psychologically grounded features like emotions, empathy and games 

# 16 October
 
## Results
- Integrated 3 components of dialogue system: Rasa, STT, TTS
- Found that the following metrics are most commonly used in evaluations/ as cost indicators:
  - Speed (latency, wall time, etc)  
  - FLOPs
  - Number of parameters

## What Went Well
- Developed a somewhat presentable system by integrating dialogue system components
- Strategised how to deal with the lack of data we have 

## What Didn't Go Well
- Underestimated how long tasks would take 

## Going Forward into Sprint 4
- Determine how to bring the user the utmost value
  - Determine whether the user values the toy's capabilites or a seamless system
- Vocoder: better user experience driven by a more enthusiastic/realistic bot voice
  - what would be ideal for the user? (Human/ robotic)
- Improved memory game: try to improve Rasa's ability to generalise (maybe adding more trainig data). Also make it function as a game (i.e. winner/ loser). 
- Develop a user interface that gives feedback to the user (lets them know that the bot is listening)
- Play around with setting up the Pi
- Debug speech to text
- Refine target audience/ age

# 23 October

## Results
- Refined the target audience (kids of age 3-6 or before grade 1)
- Improved both the memory game and math game
- Integrated games onto master

## What Went Well
- Successful meeting with Dr. Genga (supervisor) who liked our strategy for dealing with the lack of data
- Improved the games to the point of being presentable
- Clearer idea of research question and steps needed to answer it

## What Didn't Go Well
- Didn't manage to to touch all layer of the system
- Still haven't been able to start collecting results

## Going Forward into Sprint 5
- Try to balance developing "final product" for Open Day with "investigation" for report (getting results)
- Developing a final product involves:
  - Deploying to Raspberry Pi
  - Add more training data and stories
  - Open Day poster and video presentation
- Completing the investigation involves:
  - Obtaining results to reconcile observations with predictions
  - Results include: accuracy, latency, RTF (real time factor), and other qualitative and quantitative system characteristics

