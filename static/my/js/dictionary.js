+(function (w) {
    function Clazz() {
    };
    // var handles = {};
    Clazz.prototype = {
        get: function (key) {
            if (key) {
                return "";
            }
            return "";
        },
        cache: function (){},
        matchKey(datas, key, type){
            let set = datas;
            if (type) {
                set = datas[type]
            }
            for (let item of set) {
                if (item.dictKey == key){
                    return item.dictValue
                }
            }
            return "";
        },
        getByTypes:  function (dictType,option){
            let ajaxOption = {
                url:"/dict/getDictByTypes",
                type:"GET",
                // async: ,
                data: {
                    dictType: dictType
                },
                dataType:'json'
            }
            Object.assign(ajaxOption, option);
            var result = new Promise(function (resolve, reject) {
                $.ajax({
                    ...ajaxOption,
                    success: function (response) {
                        resolve(response);
                    },
                    error: function (response) {
                        reject(response);
                    }
                })
            })
            return result;
        },
        request: function (dictType){
            var result = new Promise(function (resolve, reject) {
                $.ajax({
                    url:"/dict/getDictByType",
                    type:"GET",
                    // async:false,
                    data: {
                        dictType: dictType
                    },
                    dataType:'json',
                    // success:function(result){
                    //     console.log("/dict/getDictByType : ////////// " , result)
                    // }
                    success: function (response) {
                        resolve(response);
                    },
                    error: function (response) {
                        reject(response);
                    }
                })
            })
            return result;
        }
    }
    w.dictUtils = new Clazz();
})(window);