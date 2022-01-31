
setTimeout(function () {
    window.django.jQuery(document).ready(function () {
        window.django.jQuery('#changelist-filter').addClass('sticky')

        const socket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/institutional/academiclesson/'
        );

        function ManyToManyFilter(ele_list, fun) {
            var element_list = {}

            for (let i = 0; i < ele_list.length; i++) {
                element_list[ele_list[i].substr(1)] = document.querySelector(ele_list[i]);
                element_list[ele_list[i].substr(1)].onchange = () => {
                    for (var j = 0; j < ele_list.length; j++) {
                        if (!element_list[ele_list[j].substr(1)].value) {
                            break;
                        }
                    }
                    if (j == ele_list.length) {
                        for (let k = 1; k < ele_list.length; k++) {
                            element_list[ele_list[k].substr(1)].onchange = null;
                        }
                        fun(element_list[ele_list[0].substr(1)].value)
                    }
                }
            }
        }


        // ManyToManyFilter(['#id_sub_id', '#id_class_type', '#id_slot'], function (value) {
        ManyToManyFilter(['#id_sub_id'], function (value) {
            document.querySelector('.selector-clearall').click()
            socket.send(JSON.stringify({ 'id_sub': value }))

        });

        socket.onmessage = function (e) {
            SelectBox.allow = JSON.parse(e.data)['std_ids'];
            SelectBox.redisplay('id_student_from');
        };



    });
}, 0)

