function create_source(groups, rnds){
	const group_num = groups.length;
	let columns = [];
	let idxOfRnds = [];
	let idx = 0;
	for(let i = 0; i < group_num; i++){
		for(let j = 0; j < groups[i].active.length; j++){
			columns.push(groups[i].labels[groups[i].active[j]])
			idxOfRnds.push(groups[i].active[j] + idx)
		}
		idx += groups[i].labels.length
	}
	const lines = [columns.join(',')]
	for(let m = 0; m < 2251; m++){
		let row = [];
		for(let k = 0; k < idxOfRnds.length; k++){
			if(rnds[idxOfRnds[k]].data_source.data[rnds[idxOfRnds[k]].name][m] > -1){
				row.push(rnds[idxOfRnds[k]].data_source.data[rnds[idxOfRnds[k]].name][m].toString())
			}else{
				row.push("No Data")
			}
		}
		lines.push(row.join(','))
		console.log(lines)
	}
	return lines.join('\n').concat('\n')
}

const filename = 'data_result.csv'
const filetext = create_source(groups, rnds)
console.log(filetext)
const blob = new Blob([filetext], {type: 'text/csv;charset=utf-8;'})

if(navigator.msSaveBlob){
	navigator.msSaveBlob(blob, fileName)
} else {
	const link = document.createElement('a')
	link.href = URL.createObjectURL(blob)
	link.download = filename
	link.target = '_blank'
	link.style.visibility = 'hidden'
	link.dispatchEvent(new MouseEvent('click'))
}