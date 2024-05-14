import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Injectable } from '@angular/core';
import {catchError} from 'rxjs/operators'; 

@Injectable({
  providedIn: 'root'
})
export class ReservationService {


  constructor(private http:HttpClient) { }

  getCalendar(date:string, time:string ):Observable<any>{
    var url = `https://us-central1-soa-project3.cloudfunctions.net/obtener-calendario/?date=${date}&start_time=${time}`
    return this.http.get<any>(url);
  }

  createReservation(reservation:any):Observable<any>{
    var url = 'https://us-central1-soa-project3.cloudfunctions.net/broker'
    return this.http.post<any>(url, reservation).pipe(catchError(this.handleError));
  }

  userIsValid(userToken:any):Observable<any>{
    var url = `https://us-central1-soa-project3.cloudfunctions.net/verificar-usuario/?token=${userToken}`
    return this.http.get<any>(url);
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

}
