'use strict';

function loadGroup(index) {
    $('#toappend').empty();
    $.getJSON("/group?id=" + index, function( data ) {
        let table = []
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/scoresCached?acmp=${element[0]}&timus=${element[1]}&cf=${element[2]}`, function( data ) {
                $(`
                <tr>
                    <th scope="row">Loading</th>
                    <td>${element[2]}</td>
                    <td>${data['acmp'] + data['timus'] + data['cf']}</td>
                    <td>${data['acmp']}</td>
                    <td>${data['timus']}</td>
                    <td>${data['cf']}</td>
                </tr>`).appendTo('#toappend').hide().fadeIn(200);
                table.push({name: element[2], data: data, sum: data['acmp'] + data['timus'] + data['cf']});
            }));
        });
        ps.then(() => {
            table.sort(function(a, b) { return b.sum - a.sum; });
            $('#toappend').empty();
            let rank = 1;
            table.forEach(element => {
                $(`
                <tr>
                    <th scope="row">${rank++}</th>
                    <td>${element.name}</td>
                    <td>${element.sum}</td>
                    <td>${element.data['acmp']}</td>
                    <td>${element.data['timus']}</td>
                    <td>${element.data['cf']}</td>
                </tr>`).appendTo('#toappend').hide().fadeIn(200);
            });
        });
    });
}