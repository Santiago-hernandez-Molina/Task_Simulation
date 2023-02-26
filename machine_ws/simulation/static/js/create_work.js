const addWorksForm=()=>{
	machinesN.addEventListener('input',()=>{});
	worksN.addEventListener('', ()=>{});
	let nMachines = machinesN.value;
	let nWorks = worksN.value;
	createTask(nWorks,nMachines);
}
let worksForms = document.getElementById('works-form');
let btnWork = document.getElementById('set-works');
let machinesN = document.getElementById('machines-n');
let worksN = document.getElementById('works-n');
btnWork.addEventListener('click', addWorksForm);

const createTask=(nWorks,nMachines)=>{
	if(nWorks ==0 || nMachines==0){
		alert('please select more than one');
	}else{
	  worksForms.innerHTML = "";
		let form = document.getElementById('send-data');
		let title = document.createElement('h1');
		title.innerHTML = 'Please input the time (secs) for every task';
		form.appendChild(title)
		for (let i =0; i < nWorks;i++){
			let div = document.createElement('div');
			div.className = 'text-item';
			work_title = document.createElement('h2')
			work_title.innerHTML=`work ${i}`
			div.appendChild(work_title)
			for (let j = 0 ; j < nMachines; j++){
				let input = document.createElement('input');
				input.name = `task_${i}`
				input.defaultValue = 0
				div.appendChild(input)
			}
			form.appendChild(div);
		}
		let btn_submit = document.createElement('button')
		btn_submit.type = 'submit';
		btn_submit.innerHTML = "send data";
		form.appendChild(btn_submit)
		worksForms.appendChild(form);
	}
}

