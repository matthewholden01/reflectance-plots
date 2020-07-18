function data_to_csv(source){
	const columns = Object.keys(source.data)
	const nrows = source.get_length()
	const lines = [columns.join(',')]

	for(let i = 0; i < nrows; i++){
		let row = [];
		for(let j = 0; j < columns.length; j++){
			const column = columns[j]
			row.push(source.data[column][i].toString())
		}
		lines.push(row.join(','))
	}
	return lines.join('\n').concat('\n')
}

const filename = 'data_result.csv'
const filetext = data_to_csv(source)
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