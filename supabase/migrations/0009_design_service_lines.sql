-- ============================================================================
-- BIMRACE Lead Engine — 0009 MEP engineering design service lines
--
-- The website now offers MEP engineering design (catalogue package PKG-05):
-- five new enquiry types. Design appointments carry design responsibility and
-- the highest fees, so they route to business development at high priority
-- and score as MEP/BIM project enquiries. Additive and idempotent.
-- ============================================================================

insert into crm.service_categories (code, name, description, sort_order) values
 ('mep_design','MEP Engineering Design','HVAC, plumbing, electrical and fire design with calculations',5),
 ('hvac_design','HVAC Design','Loads, ventilation, ductwork and plant design',6),
 ('plumbing_design','Plumbing Design','Water supply, drainage and pump sizing design',7),
 ('electrical_design','Electrical Design','Load assessment, distribution, SLD and lighting design',8),
 ('fire_design','Fire Protection Design','Sprinkler, hydrant and hydraulic design',9)
on conflict (code) do nothing;

update crm.lead_scoring_rules
   set value = value || ',mep_design,hvac_design,plumbing_design,electrical_design,fire_design'
 where code = 'mep_project'
   and value not like '%mep_design%';

insert into crm.lead_routing_rules
 (code, label, priority, match_lead_type, match_international, match_min_score,
  assign_to_role, set_priority) values
 ('mep_design','MEP design enquiries to business development',25,'mep_design',null,null,'business_development','high'),
 ('hvac_design','HVAC design enquiries to business development',26,'hvac_design',null,null,'business_development','high'),
 ('plumbing_design','Plumbing design enquiries to business development',27,'plumbing_design',null,null,'business_development','high'),
 ('electrical_design','Electrical design enquiries to business development',28,'electrical_design',null,null,'business_development','high'),
 ('fire_design','Fire design enquiries to business development',29,'fire_design',null,null,'business_development','high')
on conflict (code) do nothing;
