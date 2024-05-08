import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { HttpClientModule } from '@angular/common/http';
import { MatDialogModule } from '@angular/material/dialog';


@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatButtonModule,
    FormsModule,
    MatInputModule,
    HttpClientModule,
    MatDialogModule,
  ],
  exports: [
    CommonModule,
    MatButtonModule,
    FormsModule,
    MatInputModule,
    MatDialogModule,
  ]
})
export class SharedModule { }
