// Copyright (c) 2013 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

if (chrome.downloads.setShelfEnabled)
  chrome.downloads.setShelfEnabled(false);

var colors = {
  progressColor: '#0d0',
  arrow: '#555',
  danger: 'red',
  complete: 'green',
  paused: 'grey',
  background: 'white',
};

function drawLine(mtx, x1, y1, x2, y2) {
  mtx.beginPath();
  mtx.moveTo(x1, y1);
  mtx.lineTo(x2, y2);
  mtx.stroke();
}

Math.TAU = 2 * Math.PI;  

function drawProgressArc(mtx, startAngle, endAngle) {
  var center = mtx.canvas.width/2;
  mtx.lineWidth = Math.round(mtx.canvas.width*0.1);
  mtx.beginPath();
  mtx.moveTo(center, center);
  mtx.arc(center, center, center * 0.9, startAngle, endAngle, false);
  mtx.fill();
  mtx.stroke();
}

function drawUnknownProgressSpinner(mtx) {
  var center = mtx.canvas.width/2;
  const segments = 16;
  var segArc = Math.TAU / segments;
  for (var seg = 0; seg < segments; ++seg) {
    mtx.fillStyle = mtx.strokeStyle = (
      ((seg % 2) == 0) ? colors.progressColor : colors.background);
    drawProgressArc(mtx, (seg-4)*segArc, (seg-3)*segArc);
  }
}

function drawProgressSpinner(mtx, stage) {
  mtx.fillStyle = mtx.strokeStyle = colors.progressColor;
  var clocktop = -Math.TAU/4;
  drawProgressArc(mtx, clocktop, clocktop + (stage * Math.TAU));
}

function drawArrow(mtx) {
  mtx.beginPath();
  mtx.lineWidth = Math.round(mtx.canvas.width*0.1);
  mtx.lineJoin = 'round';
  mtx.strokeStyle = mtx.fillStyle = colors.arrow;
  var center = mtx.canvas.width/2;
  var minw2 = center*0.2;
  var maxw2 = center*0.60;
  var height2 = maxw2;
  mtx.moveTo(center-minw2, center-height2);
  mtx.lineTo(center+minw2, center-height2);
  mtx.lineTo(center+minw2, center);
  mtx.lineTo(center+maxw2, center);
  mtx.lineTo(center, center+height2);
  mtx.lineTo(center-maxw2, center);
  mtx.lineTo(center-minw2, center);
  mtx.lineTo(center-minw2, center-height2);
  mtx.lineTo(center+minw2, center-height2);
  mtx.stroke();
  mtx.fill();
}

function drawDangerBadge(mtx) {
  var s = mtx.canvas.width/100;
  mtx.fillStyle = colors.danger;
  mtx.strokeStyle = colors.background;
  mtx.lineWidth = Math.round(s*5);
  var edge = mtx.canvas.width-mtx.lineWidth;
  mtx.beginPath();
  mtx.moveTo(s*75, s*55);
  mtx.lineTo(edge, edge);
  mtx.lineTo(s*55, edge);
  mtx.lineTo(s*75, s*55);
  mtx.lineTo(edge, edge);
  mtx.fill();
  mtx.stroke();
}

function drawPausedBadge(mtx) {
  var s = mtx.canvas.width/100;
  mtx.beginPath();
  mtx.strokeStyle = colors.background;
  mtx.lineWidth = Math.round(s*5);
  mtx.rect(s*55, s*55, s*15, s*35);
  mtx.fillStyle = colors.paused;
  mtx.fill();
  mtx.stroke();
  mtx.rect(s*75, s*55, s*15, s*35);
  mtx.fill();
  mtx.stroke();
}

function drawCompleteBadge(mtx) {
  var s = mtx.canvas.width/100;
  mtx.beginPath();
  mtx.arc(s*75, s*75, s*15, 0, Math.TAU, false);
  mtx.fillStyle = colors.complete;
  mtx.fill();
  mtx.strokeStyle = colors.background;
  mtx.lineWidth = Math.round(s*5);
  mtx.stroke();
}

function drawIcon(side, options) {
  var canvas = document.createElement('canvas');
  canvas.width = canvas.height = side;
  document.body.appendChild(canvas);
  var mtx = canvas.getContext('2d');
  if (options.anyInProgress) {
    if (options.anyMissingTotalBytes) {
      drawUnknownProgressSpinner(mtx);
    } else {
      drawProgressSpinner(mtx, (options.totalBytesReceived /
                                options.totalTotalBytes));
    }
  }
  drawArrow(mtx);
  if (options.anyDangerous) {
    drawDangerBadge(mtx);
  } else if (options.anyPaused) {
    drawPausedBadge(mtx);
  } else if (options.anyRecentlyCompleted) {
    drawCompleteBadge(mtx);
  }
  return canvas;
}

function maybeOpen(id) {
  var openWhenComplete = [];
  try {
    openWhenComplete = JSON.parse(localStorage.openWhenComplete);
  } catch (e) {
    localStorage.openWhenComplete = JSON.stringify(openWhenComplete);
  }
  var openNowIndex = openWhenComplete.indexOf(id);
  if (openNowIndex >= 0) {
    chrome.downloads.open(id);
    openWhenComplete.splice(openNowIndex, 1);
    localStorage.openWhenComplete = JSON.stringify(openWhenComplete);
  }
}

function setBrowserActionIcon(options) {
  var canvas1 = drawIcon(19, options);
  var canvas2 = drawIcon(38, options);
  var imageData = {};
  imageData['' + canvas1.width] = canvas1.getContext('2d').getImageData(
        0, 0, canvas1.width, canvas1.height);
  imageData['' + canvas2.width] = canvas2.getContext('2d').getImageData(
        0, 0, canvas2.width, canvas2.height);
  chrome.browserAction.setIcon({imageData:imageData});
  canvas1.parentNode.removeChild(canvas1);
  canvas2.parentNode.removeChild(canvas2);
}

function pollProgress() {
  pollProgress.tid = -1;
  chrome.downloads.search({}, function(items) {
    var popupLastOpened = parseInt(localStorage.popupLastOpened);
    var options = {anyMissingTotalBytes: false,
                   anyInProgress: false,
                   anyRecentlyCompleted: false,
                   anyPaused: false,
                   anyDangerous: false,
                   totalBytesReceived: 0,
                   totalTotalBytes: 0};
    items.forEach(function(item) {
      if (item.state == 'in_progress') {
        options.anyInProgress = true;
        if (item.totalBytes) {
          options.totalTotalBytes += item.totalBytes;
          options.totalBytesReceived += item.bytesReceived;
        } else {
          options.anyMissingTotalBytes = true;
        }
        var dangerous = ((item.danger != 'safe') &&
                         (item.danger != 'accepted'));
        options.anyDangerous = options.anyDangerous || dangerous;
        options.anyPaused = options.anyPaused || item.paused;
      } else if ((item.state == 'complete') && item.endTime && !item.error) {
        options.anyRecentlyCompleted = (
          options.anyRecentlyCompleted ||
          ((new Date(item.endTime)).getTime() >= popupLastOpened));
        maybeOpen(item.id);
      }
    });

    var targetIcon = JSON.stringify(options);
    if (sessionStorage.currentIcon != targetIcon) {
      setBrowserActionIcon(options);
      sessionStorage.currentIcon = targetIcon;
    }

    if (options.anyInProgress &&
        (pollProgress.tid < 0)) {
      pollProgress.start();
    }
  });
}
pollProgress.tid = -1;
pollProgress.MS = 200;

pollProgress.start = function() {
  if (pollProgress.tid < 0) {
    pollProgress.tid = setTimeout(pollProgress, pollProgress.MS);
  }
};

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

if (!isNumber(localStorage.popupLastOpened)) {
  localStorage.popupLastOpened = '' + (new Date()).getTime();
}

chrome.downloads.onCreated.addListener(function(item) {
  pollProgress();
});

pollProgress();

function openWhenComplete(downloadId) {
  var ids = [];
  try {
    ids = JSON.parse(localStorage.openWhenComplete);
  } catch (e) {
    localStorage.openWhenComplete = JSON.stringify(ids);
  }
  pollProgress.start();
  if (ids.indexOf(downloadId) >= 0) {
    return;
  }
  ids.push(downloadId);
  localStorage.openWhenComplete = JSON.stringify(ids);
}

chrome.runtime.onMessage.addListener(function(request) {
  if (request == 'poll') {
    pollProgress.start();
  }
  if (request == 'icons') {
    [16, 19, 38, 128].forEach(function(s) {
      var canvas = drawIcon(s);
      chrome.downloads.download({
        url: canvas.toDataURL('image/png', 1.0),
        filename: 'icon' + s + '.png',
      });
      canvas.parentNode.removeChild(canvas);
    });
  }
  if (isNumber(request.openWhenComplete)) {
    openWhenComplete(request.openWhenComplete);
  }
});
