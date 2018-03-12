let dropdown = document.getElementById('selDataset');
dropdown.length = 0;

let defaultOption = document.createElement('option');
defaultOption.text = 'Choose Sample ID';

dropdown.add(defaultOption);
dropdown.selectedIndex = 0;

const url = 'http://127.0.0.1:5000/names';

fetch(url)  
  .then(  
    function(response) {  
      if (response.status !== 200) {  
        console.warn('Looks like there was a problem. Status Code: ' + 
          response.status);  
        return;  
      }

      // Examine the text in the response  
      response.json().then(function(data) {  
        let option;
    
    	for (let i = 0; i < data.length; i++) {
          option = document.createElement('option');
      	  option.text = data[i];
      	  option.value = data[i];
      	  dropdown.add(option);
    	}    
      });  
    }  
  )  
  .catch(function(err) {  
    console.error('Fetch Error -', err);  
  });