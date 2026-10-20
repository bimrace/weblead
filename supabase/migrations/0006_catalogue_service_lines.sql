-- ============================================================================
-- BIMRACE Lead Engine — 0006 catalogue service lines
--
-- The enquiry form's "What do you need" list now follows the BIMRACE service
-- catalogue (nine service lines). Each option value is the lead_type stored on
-- crm.leads, so the reference data, scoring and routing must know the codes.
--
-- Additive and idempotent, like 0001–0005: inserts use ON CONFLICT DO NOTHING,
-- and the two rule changes are guarded updates. Existing categories (mep_bim,
-- bim_modelling, …) are kept so leads already stored under them stay valid.
-- ============================================================================

insert into crm.service_categories (code, name, description, sort_order) values
 ('plumbing_bim','Plumbing BIM','Water supply, drainage, stormwater and plumbing plant modelling',11),
 ('hvac_bim','HVAC BIM','Ductwork, chilled water, VRF, ventilation and plant room modelling',12),
 ('fire_protection_bim','Fire Protection BIM','Sprinkler, hydrant, wet riser and fire pump-room modelling',13),
 ('electrical_bim','Electrical BIM','Lighting, power, containment and panel room modelling',14),
 ('bim_documentation','MEP Shop Drawings & Documentation','Shop drawings, sections, risers, builders work and registers',15),
 ('quantity_takeoff','Quantity Takeoff & BOQ','Model-based quantities, schedules, BOQs and revision comparisons',16),
 ('revit_modelling','Revit Modelling & Model Management','CAD/PDF to Revit, families, templates, worksharing and audits',17),
 ('additional_bim','As-built & Additional BIM','As-built and existing-building models, asset registers and handover',18)
on conflict (code) do nothing;
-- bim_coordination and general already exist (0004).

-- Scoring: every catalogue service line is an MEP/BIM project enquiry.
update crm.lead_scoring_rules
   set value = 'mep_bim,bim_modelling,bim_coordination,plumbing_bim,hvac_bim,fire_protection_bim,'
               'electrical_bim,bim_documentation,quantity_takeoff,revit_modelling,additional_bim'
 where code = 'mep_project'
   and value = 'mep_bim,bim_modelling,bim_coordination';

-- Routing: discipline modelling and coordination to the BIM manager queue,
-- documentation, quantities and model management to sales. Priorities slot
-- between the existing rules and before the fallback (999).
insert into crm.lead_routing_rules
 (code, label, priority, match_lead_type, match_international, match_min_score,
  assign_to_role, set_priority) values
 ('plumbing_bim','Plumbing BIM enquiries to the BIM manager queue',31,'plumbing_bim',null,null,'bim_manager','high'),
 ('hvac_bim','HVAC BIM enquiries to the BIM manager queue',32,'hvac_bim',null,null,'bim_manager','high'),
 ('fire_protection_bim','Fire protection BIM enquiries to the BIM manager queue',33,'fire_protection_bim',null,null,'bim_manager','high'),
 ('electrical_bim','Electrical BIM enquiries to the BIM manager queue',34,'electrical_bim',null,null,'bim_manager','high'),
 ('bim_documentation','Shop drawing and documentation enquiries to sales',41,'bim_documentation',null,null,'sales','normal'),
 ('quantity_takeoff','Quantity takeoff and BOQ enquiries to sales',42,'quantity_takeoff',null,null,'sales','normal'),
 ('revit_modelling','Revit modelling enquiries to sales',43,'revit_modelling',null,null,'sales','normal'),
 ('additional_bim','As-built and additional BIM enquiries to the BIM manager queue',44,'additional_bim',null,null,'bim_manager','normal')
on conflict (code) do nothing;
