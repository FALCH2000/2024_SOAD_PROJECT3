import { Component } from '@angular/core';
import { ReservationService } from '../services/reservation.service';
import { HttpClient } from '@angular/common/http';

import {FormBuilder} from '@angular/forms';

@Component({
  selector: 'app-reservation',
  templateUrl: './reservation.component.html',
  styleUrls: ['./reservation.component.scss'],
})
export class ReservationComponent {
  available_tables:any = new Array<any>();
  selected_tables:any = new Array<any>();
  selectedHour = ""
  selectedDateFormated = ""
  selectedDay = ""
  selectedTable = ""

  tables_selected = this._formBuilder.group({});


  constructor(private reservationService:ReservationService, private http: HttpClient, private _formBuilder: FormBuilder){}

  ngOnInit(): void {}



  searchTable(): void {
    const selectedDate = new Date(this.selectedDay);

    if (!isNaN(selectedDate.getTime())) {
      const year = selectedDate.getFullYear();
      const month = ('0' + (selectedDate.getMonth() + 1)).slice(-2); 
      const day = ('0' + selectedDate.getDate()).slice(-2);
      this.selectedDateFormated = `${year}-${month}-${day}`;
      this.reservationService.getCalendar(this.selectedDateFormated,this.selectedHour+":00").subscribe((data)=>{
        if(data.status === 200){
          console.log(data.data.available_tables)
          this.available_tables = data.data.available_tables;

          this.available_tables.forEach((table: { Table_ID: any; }) => {
            this.tables_selected.addControl(`table_${table.Table_ID}`, this._formBuilder.control('')); // Agrega un control al FormGroup
          });
        }
      })
    }
  }

  reserve(){

    // Obtener el valor de todas las mesas
    this.selected_tables.forEach((mesa: { Table_ID: any; Chairs: any; }) => {
      const Table_ID = mesa.Table_ID;
      const Chairs = mesa.Chairs;
      console.log(`ID de la mesa: ${Table_ID}, Sillas: ${Chairs}`);
    }); 

    
    
  }

  onCheckboxChange(event: any, table: any): void {
    if (event.checked) {
      console.log(`Checkbox para la mesa ${table.Table_ID} activado`);
      this.selected_tables.push(table);

    } else {
      console.log(`Checkbox para la mesa ${table.Table_ID} desactivado`);
      const index = this.selected_tables.indexOf(table); 
      if (index !== -1) {
        this.selected_tables.splice(index, 1); 
      }
    }
  }

  goBack(){
    this.selectedHour = "";
    this.selectedDay = "";
  }
}
