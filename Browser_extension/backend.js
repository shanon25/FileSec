//self.importScripts('test.js')

var item_url;
var item_id;
var item_paused ;
var timeIntervalId;
var fetchCount = 0;
var apiKey = 'c0cdfc9faae9ba0e5929d03b9f14e5707f87719f4ea7c68f046e1005060c2209';
var scanId ;

function handleCreated(downloadItem){
	if(downloadItem.state === 'in_progress'){

		item_url = downloadItem.url;
		item_id = downloadItem.id;
		item_paused = downloadItem.paused;

		let pausing = chrome.downloads.pause(item_id);
		pausing.then(onPaused, onError);
  	}
}

function handleChnage(downloadItem) {

	console.log(" *************** Handle change Fired");

	var item_url = downloadItem.url;
	var item_id = downloadItem.id;
	var item_paused = downloadItem.paused;
	console.log("******  file URL  : " + item_url);
	console.log("****** file item_id  : " + item_id);
	console.log("******  file item_paused  : " + item_paused);

	let pausing = chrome.downloads.pause(item_id);
	pausing.then(onPaused, onError);
	
}

chrome.downloads.onCreated.addListener(handleCreated);

 async function onPaused() {
	sendForScaning();
  }
  
  function onError(error) {
	console.log(`Error: ${error}`);
  }
  


function sendForScaning(){

	const options = {
		method: 'POST',
		headers: {
		  Accept: 'application/json',
		  'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: new URLSearchParams({
		  url: item_url,
		  apikey: apiKey
		})
	  };
	  
	fetch('https://www.virustotal.com/vtapi/v2/url/scan', options)
		.then(response => response.json())
		.then((response) => {
			console.log(' $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ scan response : ' , response);
			scanId = response.scan_id;
			timeIntervalId = setInterval(getScanReport, 15000);// change the interval as you want. currently I have set for 15seconds 
			})
		.catch((err ) => {
			cancelDownload();
			abortTimer();
			console.error(err)
  	});	
}


function getScanReport() {

	const options = {
		method: 'GET',
		headers: {Accept : 'application/json'}
	}

	var reportUrl = `https://www.virustotal.com/vtapi/v2/url/report?apikey=${apiKey}&resource=${scanId}&allinfo=false`;

	fetch(reportUrl, options)
	.then(response => response.json())
	.then((response)  => {

		var responseData = JSON.parse(JSON.stringify(response));
		console.log( " &&&&&&&&&&&&& report result : " , JSON.stringify(response));
		console.log(' ** print positives ' + responseData.positives);

		if (responseData.positives == 0) { // no malware 
			// you can return a message 
			changeLabelText(" this a test when positive = 0")
			abortTimer();// stoping the interval method execution 
			resumeDownload();
		}
		else if(responseData.positives > 0){ // when there is a malware , return an appropriate error message to your extension
			changeLabelText(" this a test when positive > 0")
			abortTimer(); // stoping the inerval method execution
			cancelDownload();
		}
	})
	.catch((err) => {
		abortTimer();
		cancelDownload();
		console.error(err)
	}); 
}

function cancelDownload(){
	chrome.downloads.cancel(item_id);
}

function resumeDownload(){
	chrome.downloads.resume(item_id);
}


function abortTimer() {
	clearInterval(timeIntervalId);
}
