import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteReservationComponent } from './delete-reservation.component';

describe('DeleteReservationComponent', () => {
  let component: DeleteReservationComponent;
  let fixture: ComponentFixture<DeleteReservationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DeleteReservationComponent]
    });
    fixture = TestBed.createComponent(DeleteReservationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
