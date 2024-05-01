function getData() {
    var xhr = new XMLHttpRequest();
    let url = document.URL.split('/')
    url = url[url.length-2]
    
    xhr.open('GET', '/Wiki/printerdcadata/' + url + "/");
    xhr.onload = function() {
        if (xhr.status === 200) {
            displayData(xhr.responseText);
        }
        else {
            alert('Request failed. Returned status of ' + xhr.status);
        }
    };
    xhr.send();
}

function displayData(data) {
    document.getElementById('data').innerHTML = data;
}

getData();