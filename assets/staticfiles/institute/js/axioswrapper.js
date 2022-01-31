function getCookie(cookiename) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split('; ');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].replace(/^\s+|\s+$/gm, '');
            if (cookie.substring(0, cookiename.length + 1) === (cookiename + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(cookiename.length + 1));
                return cookieValue
            }
        }
    }
    
}


function getHeader(form) {
    return {
        "Content-Type": "multipart/form-data; boundary=${form._boundary}",
        "X-CSRFToken": getCookie('csrftoken')
    }
}

const axiosForm = function (e, name_list = [], extra = {}) {
    var form = new FormData();
    // 'class_img': document.getElementById('id_class_img').files[0],
    // if (name_list) {
    // name_list.forEach(function (key, index) {
    for (let i = 0; i < name_list.length; i++) {
        if (e.target[name_list[i]].value) {
            if (e.target[name_list[i]].files){
                form.append(name_list[i], e.target[name_list[i]].files[0]);
            } else {
                form.append(name_list[i], e.target[name_list[i]].value);
            }
        } else if (e.target[name_list[i]][0].id) {
            form.append(name_list[i], e.target[name_list[i]][0].value);
        }
    }
    // }
    for (var key in extra) {
        form.append(key, extra[key]);
    }


    var method = e.target.attributes.method.value;
    var url = e.target.attributes.action.value;
    e.preventDefault();
    if(name_list.length > 0) {
        return new axios({
            method: method,
            url: url,
            data: form,
            headers: getHeader(form)
        })
    }
}

const axiosPost = function (url, extra={}) {
    var form = new FormData();
    for (var key in extra) {
        form.append(key, extra[key]);
    }
    return new axios.post(url, form, {
        headers: getHeader(form)
    })
}