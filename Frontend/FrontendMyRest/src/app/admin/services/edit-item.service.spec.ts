import { TestBed } from '@angular/core/testing';

import { EditItemService } from './edit-item.service';

describe('EditItemService', () => {
  let service: EditItemService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EditItemService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
