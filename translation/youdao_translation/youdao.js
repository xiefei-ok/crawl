// 引入加密模块  crypto-js
var CryptoJS = require('crypto-js')

function  get_data(query, ua){
    var ts = "" + (new Date).getTime(),
        bv = CryptoJS.MD5(ua).toString(),
        salt = ts + parseInt(10 * Math.random(), 10),
        sign = CryptoJS.MD5('fanyideskweb'+ query + salt + 'Ygy_4c=r#e#4EX^NUGUc5').toString()

    return {
        ts:ts,
        bv:bv,
        salt:salt,
        sign:sign
    }
}
// ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
// query = 'name'
//
// a = get_data(query,ua)
// console.log(a)