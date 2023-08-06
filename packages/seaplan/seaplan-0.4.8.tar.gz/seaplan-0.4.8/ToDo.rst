TO DO
======================
 
- Allow table to "line-wrap" for long comments or Action items

  - Should probably just be able to put one word/line for Actions, may
    need to be a little more clever for Comments
    
  - General table writing should be cleaner (is there a package?)
  
    HTML.py

- Fix bug that makes total estimated time too short by the length of the
  first action (because it was written assuming that the first action was
  "wait in the port")

- Fix etopo plotting and put dependencies into setup.py
    - Otherwise, sample file won't work without bath file
     
- Put actions on map in small text      

- could make event and station into classes (and events? params? table? map?)

- Allow arbitrarily long station names (or at least up to 10-15 chars),
  adapting the restructuredText table columns as needed

Use `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_ to modify this file.
