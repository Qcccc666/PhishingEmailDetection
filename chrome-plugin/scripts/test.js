var username = "13051391332"
var password = "1111111111111111111111111111111"
var webdriver = require('selenium-webdriver');
By = webdriver.By;


var driver = new webdriver.Builder().forBrowser('chrome').build();
driver.get('https://mail.163.com/')

driver.sleep(9 * 1000).then(function(){
    driver.switchTo().frame(0).then(function() {
            driver.findElement(By.className('j-inputtext dlemail')).sendKeys(username);
            driver.findElement(By.className('j-inputtext dlpwd')).sendKeys(password);
            driver.findElement(By.id('dologin')).click();
      });
})

driver.sleep(20 * 1000).then(function(){ //等待20秒
    cookie = driver.manage().getCookies().then(function(value){
        for(var i = 0; i < value.length; i++){
            if(value[i]['name'] == 'Coremail.sid'){
                break
            }    
        }
        var url = 'https://mail.163.com/js6/main.jsp?sid=' + value[i]['value'] + '&df=mail163_letter#module=read.ReadModule%7C%7B"area"%3A"normal"%2C"isThread"%3Afalse%2C"viewType"%3A""%2C"id"%3A"76%3A1tbiTB0LBlSIb4ivFAAAbc"%2C"fid"%3A1%7D'
        driver.get(url);
        driver.sleep(5 * 1000).then(function(){
            var path = "//*[@id='dvContainer']/div[2]/header/div/div[3]/div[5]"  ///div[2]/header/div[0]/div[2]/div[4]
            driver.findElement(By.xpath(path)).click();
            driver.sleep(3 * 1000).then(function(){
                //var path2 = "//*[@id='_mail_menu_8_230']/div[4]"
                var path2 = "/html/body/div[5]/div[4]"  //4为左下角
                driver.findElement(By.xpath(path2)).click();
            })
        })
    });
})

