//chrome.downloads.setShelfEnabled(false)

// chrome.downloads.onCreated.addListener(function(item) {
//   if(item.mime === "application/pdf"){
//     console.log(item)
//   } 
// });
chrome.downloads.onChanged.addListener(function(item) {
  if(item.state?.current === 'complete'){
    chrome.downloads.search(
      {id:item.id}, (file)=>{console.log(file)}
    )
  }
});

// chrome.downloads.download({
//   url:"https://dle.plymouth.ac.uk/pluginfile.php/2531442/mod_resource/content/1/CNET350SL%20MR.pdf",
//   filename: 'newpdf.pdf'
// });
