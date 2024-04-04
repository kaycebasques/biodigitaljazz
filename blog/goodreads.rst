.. _goodreads:

=========
Goodreads
=========

*2024 Apr 3*

.. raw:: html

   <p>
     Enter your Goodreads ID.
   </p>
   <input type="text" id="id" name="id" value="1090375">
   <button id="go">Go</button>
   <script>
     (async () => {
       const go = document.querySelector('#go');
       go.addEventListener('click', async () => {
         const id = document.querySelector('#id').value;
         const url = `https://www.goodreads.com/review/list_rss/${id}?shelf=read`;
         const options = {
           mode: 'cors',
           headers: {
             'Access-Control-Allow-Origin': '*'
           }
         };
         const response = await fetch(url, options);
         console.log(response);
       });
     })();
   </script>
