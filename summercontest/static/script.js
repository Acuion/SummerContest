'use strict';

$( document ).ready(function() {
    $('#github').click(() => window.location.href = 'https://github.com/Acuion/SummerContest');
    loadGroups();
    setInterval(loadGroups, 7 * 60 * 1000);
});

function appendToTable(element, rank) {
    console.log(element);
    let notsolvingStr = '';
    if (element.notsolving !== '') {
        var tmpns = element.notsolving;
        if (tmpns >= 60) {
            notsolvingStr += Math.floor(tmpns / 60) + ' ч ';
            tmpns %= 60;
        }
        notsolvingStr += tmpns + ' мин';
    }
    $(`
    <tr class="div${element.div}">
        <th scope="row">${rank}</th>
        <td>${element.name}</td>
        <td>${element.sum}</td>
        <td><a href="http://acmp.ru/index.asp?main=user&id=${element.acmpid}">${element.data['acmp']}</a></td>
        <td><a href="http://acm.timus.ru/author.aspx?id=${element.timusid}">${element.data['timus']}</a></td>
        <td>${notsolvingStr}</td>
    </tr>`).appendTo('#toappend').hide().fadeIn(200);
}

function loadGroups() {
    let totalacmp = 0, totaltimus = 0;

    $('#toappend').empty();
    appendToTable({name: 'Загрузка<br>─=≡Σ((( つ◉◡◔)つ', sum: '', data: {acmp: '', timus: ''}, div: '', notsolving: ''}, '<img src="static/Gear-1s-42px.svg"></img>');
    $.getJSON("/groups", function( data ) {
        let table = []
        let ps = Promise.resolve();
        data.forEach(element => {
            ps = ps.then(() => $.getJSON(`/solvedCached?id=${element['id']}`, function( data ) {
                let newElement = {acmpid: element['acmp'], timusid: element['timus'],
                    name: element['fio'], data: data, div: element['div'], sum: data['acmp'] + data['timus'] * 2,
                    notsolving: data['lastchange'] == -1 ? '?' : Math.round((Date.now() / 1000 - data['lastchange']) / 60)
                };
                totalacmp += data['acmp'];
                totaltimus += data['timus'];
                $('#acmp-total').text(`Acmp решено (${totalacmp})`);
                $('#timus-total').text(`Timus решено (${totaltimus})`);
                table.push(newElement);
                appendToTable(newElement, '');
            })).catch(() => {
                let newElement = {name: element['fio'] + ' (ERR)', data: {acmp: -1, timus: -1}, div: 'Err', sum: -1, incinfo: -1};
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