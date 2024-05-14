import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ScheduleService } from '../services/schedule.service';
import { Observer } from 'rxjs';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedule.component.html',
  styleUrls: ['./schedule.component.scss']
})
export class ScheduleComponent {

  selectedHourStart:string="";
  selectedHourEnd:string="";

  constructor(private scheduleService:ScheduleService, private http: HttpClient,private router:Router){}

  saveNewSchedule(){
    const registro = {
      "data":{
        "Local_ID": "1",
        "Opening_Time": this.selectedHourStart,
        "Closing_Time": this.selectedHourEnd,
      }
    }
  console.log(registro)
  this.makeRequest(registro)
  
  }
    makeRequest(registro:any){
    const observer: Observer<any> = {
      next: (data: any) => {
        if (data.status === 200) {
          alert("Disponibilidad actualizada!")
          this.router.navigate(['admin/admin-menu']);
        }
        
        console.log(data);
      },
      error: (error: any) => {
        console.error('Error occurred:', error);
        alert("Hubo un error actualizando la disponibilidad. Vuelve a intentarlo.");
        this.router.navigate(['authentication/verification']);
      },
      complete: function (): void {
        throw new Error('Function not implemented.');
      }
    };

    this.scheduleService.changeSchedule(registro).subscribe(observer);


  }

}
