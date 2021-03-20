function calc(){
    //var user = document.getElementById('user').value
	//var pass = document.getElementById('pass').value
		
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: "copy" }, function (response) {
            var win = chrome.extension.getBackgroundPage();
            win.data=response;
            //alert(win.data)
            var str = win.data
            if(str.substring(0,1) == '1'){
                var url = str.substring(10,32)
                var url1 = "https://mail.bupt.edu.cn/"+url;
                //alert(url1)
                //alert(url1)
                //下载eml
                var elemIF = document.createElement("iframe");   
                elemIF.src = url1;   
                elemIF.style.display = "none";   
                document.body.appendChild(elemIF);

                var url_pdf = str.substring(80,148)
                //alert(url_pdf)
                var elemIF = document.createElement("iframe");   
                elemIF.src = url_pdf;   
                elemIF.style.display = "none";   
                document.body.appendChild(elemIF);

                var pdfName = str.substring(148,str.indexOf('pdf')+3)
                //alert(pdfName)
                
                var name = str.substring(str.indexOf('pdf')+15,str.length)
                name = name.replace("/nbsp;/g"," ")
                //alert(name)
            }
            else{
                var url = str.substring(10,32)
                var url1 = "https://mail.bupt.edu.cn/"+url;
                //alert(url1)
                //alert(url1)
                //下载eml
                var elemIF = document.createElement("iframe");   
                elemIF.src = url1;   
                elemIF.style.display = "none";   
                document.body.appendChild(elemIF);

                var name = str.substring(80,str.length)
                name = name.replace("/nbsp;/g"," ")
                //alert(name)
                var pdfName = 1
            }
            
            postLast(name,pdfName)

        });  
    }); 

    /*<a href="read.php?dmid=40697756" target="download_frname" hidefocus="">导出邮件</a>ICIIT&nbsp;2019-Paper&nbsp;ID:&nbsp;D2032
    */
    /* 
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // 发送一个copy消息出去
            chrome.tabs.sendMessage(tabs[0].id, { action: "copy" }, function (response) {
      // 这里的回调函数接收到了要抓取的值，获取值得操作在下方content-script.js
      // 将值存在background.js的data属性里面。
                //var win = chrome.extension.getBackgroundPage();
                //win.data=response;
                alert(response);
            });  
        }); */
}


function postBack(flag,name){
    alert('感谢你的反馈，我们会及时改进我们的系统！')
    var ajax = new XMLHttpRequest();
    ajax.open('get','http://localhost:8089/back?'+'name='+name+'&flag='+flag);
    ajax.send()
    ajax.onreadystatechange = function () {
        if (ajax.readyState==4 &&ajax.status==200) {
            //步骤五 如果能够进到这个判断 说明 数据 完美的回来了,并且请求的页面是存在的
        　　　　 //alert(ajax.responseText);//输入相应的内容
            //alert(this.response)
            //alert('1111')
        }
    }
}




function postLast(name,pdfname){
    var ajax = new XMLHttpRequest();
    var b = new Base64();
    var name_str = b.encode(name); 
    ajax.open('get','http://localhost:8089/get_url1?'+'name='+name_str+'&pdfname='+pdfname);
    ajax.send()
    ajax.onreadystatechange = function () {
        if (ajax.readyState==4 &&ajax.status==200) {
            //alert(this.response)
            //alert(this.response.feature)
            //alert(this.response.substring(0,10))
            var temp = this.response.split(',');
            //alert(temp[0]);
            //alert(temp[1]);
            //alert(temp);
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { action: temp }, function (response) {
                    //alert('11111')
                    var win = chrome.extension.getBackgroundPage();
                    win.data=response;
                    //alert(win.data)
                    var str = win.data
                    var flag = str.substring(0,1);
                    var name = str.substring(1,str.length)
                    //alert('begin postback')
                    //postBack(flag,name)
                });  
            }); 
        }
    }
}


function post(name,url,user,pass){
	var ajax = new XMLHttpRequest();
	var b = new Base64();
    var str = b.encode(url);  
    var name_str = b.encode(name); 
    //var str = url
//步骤二:设置请求的url参数,参数一是请求的类型,参数二是请求的url,可以带参数,动态的传递参数starName到服务端
	ajax.open('get','http://localhost:8089/get_url?username='+user+'&password='+pass+'&name='+name_str+'&url='+str);
	//步骤三:发送请求
	ajax.send();
	//步骤四:注册事件 onreadystatechange 状态改变就会调用
	ajax.onreadystatechange = function () {
	if (ajax.readyState==4 &&ajax.status==200) {
		//步骤五 如果能够进到这个判断 说明 数据 完美的回来了,并且请求的页面是存在的
    　　　　 //alert(ajax.responseText);//输入相应的内容
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, { action: ajax.responseText }, function (response) {
                    console.log(111)
                });  
            }); 
	　　}
	}
	
}



/*
chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
	console.log(tabs[0].url);
	var str = "https://mail.163.com"; 
	if(tabs[0].url.search(str) >= 0){
		//python搭建web服务器
		post(tabs[0].url)
	}
});
*/
var oBtn= document.getElementById("calcBtn");
oBtn.onclick=function(){
	calc()
}

//var text= document.getElementById("7");
///var oBtn1= document.getElementById("back");
//oBtn1.onclick=function(){
//	back1(text)
//}


function Base64() {
 
    // private property
    _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
 
    // public method for encoding
    this.encode = function (input) {
        var output = "";
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        var i = 0;
        input = _utf8_encode(input);
        while (i < input.length) {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }
            output = output +
            _keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
            _keyStr.charAt(enc3) + _keyStr.charAt(enc4);
        }
        return output;
    }
 
    // public method for decoding
    this.decode = function (input) {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (i < input.length) {
            enc1 = _keyStr.indexOf(input.charAt(i++));
            enc2 = _keyStr.indexOf(input.charAt(i++));
            enc3 = _keyStr.indexOf(input.charAt(i++));
            enc4 = _keyStr.indexOf(input.charAt(i++));
            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;
            output = output + String.fromCharCode(chr1);
            if (enc3 != 64) {
                output = output + String.fromCharCode(chr2);
            }
            if (enc4 != 64) {
                output = output + String.fromCharCode(chr3);
            }
        }
        output = _utf8_decode(output);
        return output;
    }
 
    // private method for UTF-8 encoding
    _utf8_encode = function (string) {
        string = string.replace(/\r\n/g,"\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            } else if((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            } else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
 
        }
        return utftext;
    }
 
    // private method for UTF-8 decoding
    _utf8_decode = function (utftext) {
        var string = "";
        var i = 0;
        var c = c1 = c2 = 0;
        while ( i < utftext.length ) {
            c = utftext.charCodeAt(i);
            if (c < 128) {
                string += String.fromCharCode(c);
                i++;
            } else if((c > 191) && (c < 224)) {
                c2 = utftext.charCodeAt(i+1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            } else {
                c2 = utftext.charCodeAt(i+1);
                c3 = utftext.charCodeAt(i+2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }
        }
        return string;
    }
}



