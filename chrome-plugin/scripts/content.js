chrome.extension.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.action === "copy") {
            var tables = document.getElementById('main').contentWindow.document.getElementsByTagName('li');
            //tables[12].click();
            console.log(tables[12]);
            var tables1 = document.getElementById('main').contentWindow.document.getElementsByTagName('h2');
            console.log(tables1[1].innerHTML);
            var str = tables[12].innerHTML + tables1[1].innerHTML
            var tables2 = document.getElementById('main').contentWindow.document.getElementsByTagName('a');
            var tables3 = document.getElementById('main').contentWindow.document.getElementsByTagName('div');
            //console.log(tables3[197]);
            console.log(tables2);
            console.log(tables3);
            console.log(tables2[125].href);
            console.log(tables3[187].innerText);
            if(tables3[187].innerText.indexOf('pdf') == -1){
                var str = '0'+tables[12].innerHTML + tables1[1].innerHTML
            }
            else{
                var str = '1'+tables[12].innerHTML + tables2[125].href + tables3[187].innerText + tables1[1].innerHTML
            }
            //var str = tables[12].innerHTML + tables2[125].href + tables3[187].innerText + tables3[187].innerText
            sendResponse(str);
        }
        else{
            var tables1 = document.getElementById('main').contentWindow.document.getElementsByTagName('h2');
            var name = tables1[1].innerHTML
            console.log(request.action);
            var i = 0;
            var j = 0;
            var arrayTemp = new Array();
            //alert(request.action.length)
            for(i = 0; i < request.action.length-1; i++){
                if(i == 0){
                    //alert('!!!!!!!!!!!!!!!!!')
                    arrayTemp[j] = request.action[i].substring(request.action[i].length-3,request.action[i].length-1);
                    j++;
                }
                else if(i == request.action.length-2){
                    arrayTemp[j] = request.action[i].substring(request.action[i].indexOf("\"")+1,request.action[i].length-5);
                    j++;
                }
                else if(request.action[i].indexOf("\"") != -1){
                    //alert(1111111111111111111111111111111111111111)
                    arrayTemp[j] = request.action[i].substring(request.action[i].indexOf("\"")+1,request.action[i].length-1);
                    j++;
                }
                else{
                    arrayTemp[j] = request.action[i].substring(request.action[i].indexOf("\n")+1,request.action.length-1)
                    j++;
                }
            }
            var str19 = '   测试结果为：'+request.action[request.action.length-1].substring(request.action[i].indexOf(":")+3,request.action[i].indexOf("}")-2)+'\n';
            console.log(arrayTemp)
            //alert(name)
            //var str = '结果与实际是否符合？此调查仅用于模型的调整'
            var str1 = '   标题含有黑名单关键词：                           '+arrayTemp[0]+'\n';
            var str2 = '   发件人地址和回复人地址是否相同：          '+arrayTemp[1]+'\n';
            var str3 = '   发件人域名和Message-Id域名是否相同：  '+arrayTemp[2]+'\n';
            var str4 = '   是否为html格式邮件：                             '+arrayTemp[3]+'\n';
            var str5 = '   是否包含Ip格式URL                                 '+arrayTemp[4]+'\n';
            var str6 = '   是否包含图片URL：                                 '+arrayTemp[5]+'\n';
            var str7 = '   是否包含异常端口：                                 '+arrayTemp[6]+'\n';
            var str8 = '   %的数量：                                          '+arrayTemp[7]+'\n';
            var str9 = '   @的数量：                                          '+arrayTemp[8]+'\n';
           var str10 = '   .的数量：                                             '+arrayTemp[9]+'\n';
           var str11 = '   URL的数量：                                         '+arrayTemp[10]+'\n';
           var str12 = '   域名的数量：                                        '+arrayTemp[11]+'\n';
           var str13 = '   实际指向的URL和显示的URL是否相同：      '+arrayTemp[12]+'\n';
           var str14 = '   是否包含JS脚本：                                     '+arrayTemp[13]+'\n';
           var str15 = '   是否更改浏览器状态栏：                            '+arrayTemp[14]+'\n';
           var str16 = '   是否更改pop-up：                                    '+arrayTemp[15]+'\n';
           var str17 = '   是否更改on-Click：                                  '+arrayTemp[16]+'\n';
            var str18 = '   ****[?]该判定结果是否与实际一致[确定(一致)，取消(不一致)]****\n   ';
            var str =  str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + str10 + str11 + str12 + str13 + str14 + str15 + str16 + str17+ str19 + str18;
            var flag = confirm(str);
            // if(flag){
            //     alert("你点击的是确定");
            //     var str = '1' + name;
            // }
            // else{
            //     alert("你单击的是取消");	
            //     var str = '0' + name
            // }

            //var str = flag.toString + name;
            //sendResponse(str);
            postBack(flag,name)
            //alert(request.action)
        }
        //73-82
    }
);

function postBack(flag,name){
    var ajax = new XMLHttpRequest();
    ajax.open('get','http://localhost:8089/back?'+'name='+name+'&flag='+flag);
    ajax.send()
    ajax.onreadystatechange = function () {
        if (ajax.readyState==4 &&ajax.status==200) {
            //步骤五 如果能够进到这个判断 说明 数据 完美的回来了,并且请求的页面是存在的
        　　　　 //alert(ajax.responseText);//输入相应的内容
            alert(this.response)
        }
    }
}