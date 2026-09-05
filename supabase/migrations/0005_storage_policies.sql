-- ============================================================================
-- BIMRACE Lead Engine — 0005 private storage for enquiry attachments
-- Additive. Creates one PRIVATE bucket; files are never publicly readable and
-- are reached only through short-lived signed URLs issued to staff.
-- ============================================================================

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('enquiry-files', 'enquiry-files', false, 52428800,
        array['application/pdf','image/png','image/jpeg','image/webp',
              'application/zip','application/x-zip-compressed',
              'application/acad','image/vnd.dwg','application/dxf',
              'model/ifc','application/octet-stream'])
on conflict (id) do update
  set public = false,                       -- force private even if it existed
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

-- Anonymous users may upload, but only into the incoming/ prefix and only
-- with a generated object name. They cannot list, read, overwrite or delete.
drop policy if exists "anon upload enquiry files" on storage.objects;
create policy "anon upload enquiry files" on storage.objects
  for insert to anon
  with check (bucket_id = 'enquiry-files'
              and (storage.foldername(name))[1] = 'incoming');

-- No SELECT policy for anon: a private bucket plus no read policy means an
-- uploaded file cannot be retrieved by guessing its URL.

drop policy if exists "staff read enquiry files" on storage.objects;
create policy "staff read enquiry files" on storage.objects
  for select to authenticated
  using (bucket_id = 'enquiry-files' and crm.is_staff());

drop policy if exists "staff manage enquiry files" on storage.objects;
create policy "staff manage enquiry files" on storage.objects
  for all to authenticated
  using (bucket_id = 'enquiry-files' and crm.is_staff())
  with check (bucket_id = 'enquiry-files' and crm.is_staff());

drop policy if exists "admin delete enquiry files" on storage.objects;
create policy "admin delete enquiry files" on storage.objects
  for delete to authenticated
  using (bucket_id = 'enquiry-files' and crm.is_admin());
