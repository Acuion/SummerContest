'use strict';

$( document ).ready(function() {
    $('#old').click(() => loadGroup(1));
    $('#new').click(() => loadGroup(2));
    $('#school').click(() => loadGroup(3));
    $('#github').click(() => window.location.href = 'https://github.com/Acuion/SummerContest');
});

function appendToTable(element, rank) {
    $(`
    <tr>
        <th scope="row">${rank}</th>
        <td>${element.name}</td>
        <td>${element.sum}</td>
        <td>${element.data['acmp']}</td>
        <td>${element.data['timus']}</td>
        <td>${element.data['cf']}</td>
    </tr>`).appendTo('#toappend').hide().fadeIn(200);
}

function loadGroup(index) {
    $('#toappend').empty();
    appendToTable({name: 'Таблица загружается', sum: 0, data: {acmp: 0, timus: 0, cf: 0}}, '<img src="static/Gear-1s-42px.svg"></img>');
    $.getJSON("/group?id=" + index, function( data ) {
        let table = []
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/scoresCached?acmp=${element[0]}&timus=${element[1]}&cf=${element[2]}`, function( data ) {
                let newElement = {name: element[2], data: data, sum: data['acmp'] + data['timus'] + data['cf']};
                table.push(newElement);
                appendToTable(newElement, '');
            }));
        });
        ps.then(() => {
            table.sort(function(a, b) { return b.sum - a.sum; });
            $('#toappend').empty();
            let rank = 1;
            table.forEach(element => appendToTable(element, rank++));
        });
    });
}