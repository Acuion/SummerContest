'use strict';

$( document ).ready(function() {
    $('#github').click(() => window.location.href = 'https://github.com/Acuion/SummerContest');
    loadGroups();
});

function appendToTable(element, rank) {
    console.log(element);
    $(`
    <tr class="div${element.div}">
        <th scope="row">${rank}</th>
        <td>${element.name}</td>
        <td>${element.sum}</td>
        <td>${element.data['acmp']}</td>
        <td>${element.data['timus']}</td>
        <td>${element.data['cfdiv1']}</td>
        <td>${element.data['cfdiv23']}</td>
    </tr>`).appendTo('#toappend').hide().fadeIn(200);
}

function loadGroups() {
    $('#toappend').empty();
    appendToTable({name: 'Загрузка ─=≡Σ((( つ◉◡◔)つ', sum: 0, data: {acmp: 0, timus: 0, cfdiv1: 0, cfdiv23: 0}, div: ''}, '<img src="static/Gear-1s-42px.svg"></img>');
    $.getJSON("/groups", function( data ) {
        let table = []
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/solvedCached?acmp=${element['acmp']}&timus=${element['timus']}&cf=${element['cf']}`, function( data ) {
                let newElement = {name: element['fio'], data: data, div: element['div'], sum: data['acmp'] + data['timus'] * 2 + data['cfdiv1'] * 10 + data['cfdiv23'] * 5};
                table.push(newElement);
                appendToTable(newElement, '');
            })).catch(() => {
                let newElement = {name: element['fio'] + ' (ERR)', data: {acmp: -1, timus: -1, cfdiv1: -1, cfdiv23: -1}, div: 'Err', sum: 0};
                table.push(newElement);
                appendToTable(newElement, '');
            });
        });
        ps.then(() => {
            table.sort(function(a, b) { return b.sum - a.sum; });
            $('#toappend').empty();
            let rank = 1;
            table.forEach(element => appendToTable(element, rank++));
        });
    });
}