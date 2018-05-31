'use strict';

function loadGroup(index) {
    $.getJSON("/group?id=" + index, function( data ) {
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/scoresCached?acmp=${element[0]}&timus=${element[1]}&cf=${element[2]}`, function( data ) {
                $('#toappend').append(`
                <tr>
                    <th scope="row">...</th>
                    <td>${element[2]}</td>
                    <td>${data['acmp'] + data['timus'] + data['cf']}</td>
                    <td>${data['acmp']}</td>
                    <td>${data['timus']}</td>
                    <td>${data['cf']}</td>
                </tr>`);
            }));
        });
    });
}