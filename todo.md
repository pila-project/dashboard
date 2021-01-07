 
## Sprint 13/10

 - ### table with filterable columns and aggregate
 - ### create number of attempts per task (conditional formatting if success)
 - ### average time per task (ref. to end a task)
 - ### average number of actions per task
 - ### class graph
 - ### dictionary for instructions
  
 
 ### Ending a task:
 1. run_done success (unsuccess is not ending a task)
 2. [return to dashboard (i.e. abort)] not implemented yet
 3. time limit (encompassing end session)
 


 ### Technical components
 - Production server (nginx and gunicorn)
 - login from PILA 
 
 ### Content
  - Indicators 
  - Text content
  - API from Jason
 
### Improvements
 - update readme 
 - alpine/python image
 - UI
 - wrap it into cloud build with github actions 
- caching 
- auto-sizing divs based on browser window size
- Nosql for instructions

karel duplicate block

What Karel is well-suited for: its limited programming vocabulary,
 and use of not-conventional programming constructs (pick up stone), 
 affords to measure how students decompose problems into subproblems, 
 what modular pieces are there, the sequence of defining algorithms 
 and debugging algorithms (in a very visually recognizable way - 
 the execution itself lends itself well to debugging).
  That’s in contrast to someone who shows their understanding of what
   a variable is. → Much more aligned with the process relevant to
    computational thinking and problem-solving: Match a goal state. 
    
Is there a way to quantify the task completion e.g. 
in terms of % stones picked up, or measure of time: 
How far have they progressed over a certain amount of time. 

