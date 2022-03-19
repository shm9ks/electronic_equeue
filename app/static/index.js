var requestURL = 'http://127.0.0.1:5000/api/get/queue';
var request = new XMLHttpRequest();
request.open('GET', requestURL);
request.responseType = 'json';
request.send();
request.onload = function() {
  var data = request.response;
  equeue(data);
}

function equeue(jsonObj) {
console.log(jsonObj);
console.log(typeof(jsonObj));
console.log(Object.keys(jsonObj));
console.log(typeof(Object.keys(jsonObj)));
for (var i in jsonObj){
    if (!isNaN(parseFloat(i)) && isFinite(i)){
        console.log("Пришло число");
        console.log("jsonObj." + i + " = " + jsonObj[i]);
    } else{
        console.log('Пришло не число, вероятно ошибка(error, смотри api - routes.py)');
        console.log(i);
    }
}
}
