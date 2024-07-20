.. _diff2html:

============================
diff2html + GitHub API = ???
============================

*2024 Jul 20*

.. _Get a commit: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#get-a-commit

This is just a quick & dirty (yeehaw) post to get community feedback on whether
"I'm holding this thing correctly." If anything useful comes out of the
discussion I will be a good OSSamaritan and translate into PRs, issues,
feature requests, etc.

I'm trying to use `diff2html <https://diff2html.xyz>`__ and the GitHub API
together. That is, I pull commit data with the `Get a commit`_ endpoint
and want to render the diff with diff2html.

I get commit data like this:

.. code-block:: js

   // Example commit that demonstrates almost all the ways you can change a file
   const url = 'https://api.github.com/repos/kaycebasques/biodigitaljazz/commits/f0a19c4d1d9267669dcc0c124387e057cbda83ac';
   const headers = {
     'X-GitHub-Api-Version': '2022-11-28',
     'Accept': 'application/vnd.github+json'
   };
   const response = await fetch(url, headers);
   const data = await response.json();
   console.log(data);

.. _demo commit: https://github.com/kaycebasques/biodigitaljazz/commit/f0a19c4d1d9267669dcc0c124387e057cbda83ac

The GitHub endpoint lists a bunch of different ways that a file
can change:

* ``added``
* ``removed``
* ``modified``
* ``renamed``
* ``copied``
* ``changed``
* ``unchanged``

I created a `demo commit`_ to attempt to trigger all the change types
but couldn't figure out the last threee (``copied``, ``changed``, and
``unchanged``).

Here's the thing that I feel I'm holding wrong. On my naive first attempt,
I basically passed the commit data from GitHub directly to diff2html,
but nothing got rendered. On closer inspection it seems that diff2html expects
more metadata than what GitHub provides. I concluded that I need to manually assembly
the diff data into the format that diff2html expects.

.. code-block:: js

   // Construct the diff string in the "unified format" that diff2html requires
   const parentCommitSha = data.parents[0].sha;
   let diffLines = [];
   for (let i = 0; i < data.files.length; i++) {
     const file = data.files[i];
     const {sha, filename, patch} = file;
     // 100644 means non-executable file which may not always be true but there doesn't
     // seem to be a way to extract file mode from this GitHub endpoint
     const fileMode = '100644';
     switch (file.status) {
       case 'added':
         diffLines.push(`diff --git a/${filename} b/${filename}`);
         diffLines.push(`new file mode ${fileMode}`);
         diffLines.push(`index 000000000..${parentCommitSha}`);
         diffLines.push(`--- /dev/null`);
         diffLines.push(`+++ b/${filename}`);
         break;
       case 'removed':
         diffLines.push(`diff --git a/${filename} b/${filename}`);
         diffLines.push(`deleted file mode ${fileMode}`);
         diffLines.push(`index ${sha}..000000000`);
         diffLines.push(`--- a/${filename}`);
         diffLines.push(`+++ /dev/null`);
         break;
       case 'renamed':   
         const previousFilename = file.previous_filename;
         diffLines.push(`diff --git a/${previousFilename} b/${filename}`);
         diffLines.push(`similarity index 100%`);
         diffLines.push(`rename from ${previousFilename}`);
         diffLines.push(`rename to ${filename}`);
         break;
       case 'copied':  // ???
       case 'changed':  // ???
       case 'unchanged':  // ???
       case 'modified':
         diffLines.push(`diff --git a/${filename} b/${filename}`);
         diffLines.push(`index ${sha}..${parentCommitSha}`);
         diffLines.push(`--- a/${filename}`);
         diffLines.push(`+++ b/${filename}`);
         break;
     }
     if (patch) {
       diffLines.push(patch); 
     }
   }
   const diffString = diffLines.join('\n');
   console.log(diffString);

So am I actually supposed to manually construct the diff strings like this?
Or is there some way to finagle the GitHub API into providing the data in the
way that diff2html expects? Or maybe I missed a way to pass the GitHub API data
directly to diff2html and let diff2html assemble it?

(For sake of completeness) here's how I render with diff2html:

.. code-block:: js

   var targetElement = document.getElementById('myDiffElement');
   var configuration = {
     drawFileList: false,
     fileListToggle: false,
     fileListStartVisible: false,
     fileContentToggle: false,
     matching: 'lines',
     outputFormat: 'line-by-line',
     synchronisedScroll: true,
     highlight: true,
     renderNothingWhenEmpty: false,
   };
   var diff2htmlUi = new Diff2HtmlUI(targetElement, diffString, configuration);
   diff2htmlUi.draw();
   diff2htmlUi.highlightCode();

* `Full demo source code <https://glitch.com/edit/#!/diff2html-github?path=index.html>`_
* `Full demo preview <https://diff2html-github.glitch.me>`_
