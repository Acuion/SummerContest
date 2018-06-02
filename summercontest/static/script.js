'use strict';

$( document ).ready(function() {
    $('#github').click(() => window.location.href = 'https://github.com/Acuion/SummerContest');
    loadGroups();
});

function appendToTable(element, rank) {
    console.log(element);
    $(`
    <tr>
        <th scope="row">${rank}</th>
        <td>${element.name} (${element.div})</td>
        <td>${element.sum}</td>
        <td>${element.data['acmp']}</td>
        <td>${element.data['timus']}</td>
        <td>${element.data['cfDiv1']}</td>
        <td>${element.data['cfDiv23']}</td>
    </tr>`).appendTo('#toappend').hide().fadeIn(200);
}

function loadGroups() {
    $('#toappend').empty();
    appendToTable({name: 'Загрузка', sum: 0, data: {acmp: 0, timus: 0, cfDiv1: 0, cfDiv23: 0}, div: '─=≡Σ((( つ◉◡◔)つ'}, '<img src="static/Gear-1s-42px.svg"></img>');
    $.getJSON("/groups", function( data ) {
        let table = []
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/solvedCached?acmp=${element['acmp']}&timus=${element['timus']}&cf=${element['cf']}`, function( data ) {
                let newElement = {name: element['fio'], data: data, div: element['div'], sum: data['acmp'] + data['timus'] * 2 + data['cfDiv1'] * 10 + data['cfDiv23'] * 5};
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