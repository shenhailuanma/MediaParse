// JavaScript Document
function http_post(url, data, type, success_func) {
	var ajax = $.ajax({
		type: type,
		url: url,
		timeout: 5000,
		data: data,
		success: success_func, 
		dataType: 'json',
		async: true,
	});
}

function delete_task(task_id) {
	var ajax = $.ajax({
		type: "POST",
		url: '/api/task/delete',
		data: {'task_id': task_id},
		success: function(data) {
			
			//alert(data);
			location.reload();
		}, 
		dataType: 'json',
		async: true,
	});
}