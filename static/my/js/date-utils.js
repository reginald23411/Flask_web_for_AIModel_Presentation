+(function (w) {
    function Clazz() {
    };
    // var handles = {};
    Clazz.prototype = {
        format: function formatDate(now,dateFormat) {

            now = new Date(now);
            dateFormat = dateFormat || "yyyy-MM-dd HH:mm:ss";
            var year = now.getFullYear();

            var month = now.getMonth() + 1;
            if( month < 10 ){
                month = '0'+ month;
            }
            var date = now.getDate();
            if( date < 10 ){
                date = '0'+ date;
            }
            var hour = now.getHours();
            if( hour < 10 ){
                hour = '0'+ hour;
            }
            var minute = now.getMinutes();
            if( minute < 10 ){
                minute = '0'+ minute;
            }
            var second = now.getSeconds();
            if( second < 10 ){
                second = '0'+ second;
            }
            //return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
            dateFormat = dateFormat.replace(/yyyy/g,year).replace(/MM/g,month).replace(/dd/g,date).replace(/HH/g,hour).replace(/mm/g,minute).replace(/ss/g,second);
            return dateFormat;
        }
    }
    w.dateUtils = new Clazz();
})(window);