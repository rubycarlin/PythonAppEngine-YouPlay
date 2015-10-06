console.log("start");
var count = 0;
var p_tag = document.getElementsByTagName('p');
var h3_tag = document.getElementsByTagName('h3');
var finished = false;
/*function next_video(){
	while(count < p_tag.length){
		console.log(p_tag[count].innerHTML);
		var ready = false;
		while(finished == false){
			// 2. This code loads the IFrame Player API code asynchronously.
			var iframe = document.getElementById('player');
			var src_url = "https://www.youtube.com/embed/" + p_tag[count].innerHTML + "?enablejsapi=1";

			console.log(iframe.src);
			if(ready == false){
				onYouTubeIframeAPIReady();
			}
			else{
				ready = true;
			}
					

			var player;

		}
	}
}*/
/*
$(function() {
    
    var url = h3_tag[count].innerHTML;
    console.log(url);
    getJSON('/getlyric', {
          lyricurl: url
        }, function(data) {
          console.log(data.lyrics);
    });
});
*/
function onYouTubeIframeAPIReady(src_url) {
	console.log("iframe ready");
	console.log(p_tag[count].innerHTML);
	var lyric_url = h3_tag[count].innerHTML;
	console.log(lyric_url);
	$.ajax({
	  		url: "/getlyric",
	  		type: 'POST',
	  		data: {'lyricurl' : lyric_url},
	  		success: function(data){
	  			console.log("Success")
	  			console.log(data)
	  			var lyric_box_tag = document.getElementById("lyricbox");
	  			/*var para = document.createElement("P");
	  			var t = document.createTextNode(data);
	  			para.appendChild(t);
	  			lyric_box_tag.appendChild(para); */
	  			lyric_box_tag.innerHTML = data;
	    		//console.log(data.lyrics)
  		}
	});
	player = new YT.Player( 'player', {
		height: '390',
		width: '640',
		videoId: p_tag[count].innerHTML,
		events: { 'onStateChange': onPlayerStateChange,
				  'onReady': onPlayerReady
			 }
	});
}
function onPlayerReady(event) {
  event.target.playVideo();
}
function onPlayerStateChange(event) {
	switch(event.data) {
		case 0:
			//Video ended
			count += 1;
			finished = true;
			console.log("Video ended");
			
			console.log("Next video");
			console.log(p_tag[count].innerHTML);
			
			var lyric_url = h3_tag[count].innerHTML;
			console.log(lyric_url);
			$.ajax({
			  		url: "/getlyric",
			  		type: 'POST',
			  		data: {'lyricurl' : lyric_url},
			  		success: function(data){
			  			console.log("Success")
			  			console.log(data)
			  			var lyric_box_tag = document.getElementById("lyricbox");
			  			/*var para = document.createElement("P");
			  			var t = document.createTextNode(data);
			  			para.appendChild(t);*/
			  			lyric_box_tag.innerHTML = data;
			    		//console.log(data.lyrics)
		  		}
			});
			player.loadVideoById({videoId:p_tag[count].innerHTML})
			break;
		case 1:
			//Still playing
			console.log("video playing");
			break;
		case 2:
			//paused
			console.log("video paused");
			break;
	}
}

	

