// JavaScript Document
var intervalTime = 1100; //监控频率
var is_start = true; //已经开始监控
var chart_data_length = 256; //图上的点数

function _to_time_format(s) {
	s = s + '';
	var l = (s + '').length;
	if (l == 1) return '0' + s;
	else if (l == 2) return s;
	else return '00';
}
//当前时间，24h
function current_time(d) {
	if (d == null || d == 'undefine') {
		d = new Date();
	}
	return _to_time_format(d.getHours()) + ':' + _to_time_format(d.getMinutes()) + ':' + _to_time_format(d.getSeconds());
}

function monitor_task() {
	if (is_start) {
		get_server_data();
    }
	else {
		setTimeout(monitor_task, intervalTime);
	}
}

function sec_2_hour(sec) {
	var h = parseInt(sec / 3600);
	var m = parseInt((sec - h * 3600) / 60)
	var s = sec - h * 3600 - m * 60;
	return h + ':' + m + ':' + s;
}

var echarts = null;

var timechart = null;
var opschart = null;
var memchart = null;
var cpuchart = null;
require.config({
    paths: {
        echarts: '/static/lib/echarts/'
    }
});
// 按需加载
require([
        'echarts',
        'echarts/chart/line',
        'echarts/chart/bar',
    ],
    function(ec) {
		echarts = ec;
	
		cpuchart = draw_chart('cpu_chart', get_line_option('Redis Cpu Usage', '', ['cpu_user', 'cpu_sys', 'cpu_user_children', 'cpu_sys_children'], 'Cpu Usage', ''));
		//开启监控
		//var r = check_redis_exist();
		if (true) {
			monitor_task();
		}
    }
);
function draw_chart(e_id, option) {
	var eChart = echarts.init(document.getElementById(e_id));
	eChart.setOption(option);
	return eChart
}