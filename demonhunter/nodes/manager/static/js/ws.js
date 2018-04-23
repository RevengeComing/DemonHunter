function show_notif(type, title, content){
	$('.notification-box').removeClass('hidden');
	$('#notif-title').html(title);
	$('#notif-content').html(content);
	$('.notif-type').addClass(type)
}

$(document).ready(function(){
    var socket = new WebSocket('ws://' + document.domain + ':' + location.port + '/notifications/');
    socket.onmessage = function (event) {
    	var data = JSON.parse(event.data);
    	console.log(data);
        show_notif(data.type, data.title, data.content);
    }
});