var request = new XMLHttpRequest();


request.onreadystatechange = function () {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        var response = this.responseText;
        console.log(response);
    }
}
request.open("GET", "{% url 'boutique:boutique' %}");
request.send();

