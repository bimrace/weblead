-- ============================================================================
-- BIMRACE Lead Engine — 0004 seed reference data
-- Idempotent: every insert uses ON CONFLICT DO NOTHING, so re-running is safe.
-- ============================================================================

insert into crm.countries (code, name, region, is_target, currency, default_tz) values
 ('IN','India','South Asia',true,'INR','Asia/Kolkata'),
 ('AE','United Arab Emirates','Middle East',true,'AED','Asia/Dubai'),
 ('SA','Saudi Arabia','Middle East',true,'SAR','Asia/Riyadh'),
 ('QA','Qatar','Middle East',true,'QAR','Asia/Qatar'),
 ('GB','United Kingdom','Europe',true,'GBP','Europe/London'),
 ('US','United States','North America',true,'USD','America/New_York'),
 ('CA','Canada','North America',true,'CAD','America/Toronto'),
 ('AU','Australia','Oceania',true,'AUD','Australia/Sydney'),
 ('SG','Singapore','South East Asia',true,'SGD','Asia/Singapore'),
 ('DE','Germany','Europe',false,'EUR','Europe/Berlin'),
 ('NL','Netherlands','Europe',false,'EUR','Europe/Amsterdam'),
 ('OM','Oman','Middle East',false,'OMR','Asia/Muscat'),
 ('KW','Kuwait','Middle East',false,'KWD','Asia/Kuwait'),
 ('NZ','New Zealand','Oceania',false,'NZD','Pacific/Auckland')
on conflict (code) do nothing;

insert into crm.lead_sources (code, name, sort_order) values
 ('website','Website',10),('google_search','Google Search',20),
 ('google_business','Google Business Profile',30),('linkedin','LinkedIn',40),
 ('referral','Referral',50),('direct_email','Direct Email',60),('phone','Phone',70),
 ('campaign','Campaign',80),('partner','Partner',90),('advertisement','Advertisement',100),
 ('other','Other',999)
on conflict (code) do nothing;

insert into crm.service_categories (code, name, description, sort_order) values
 ('bim_modelling','BIM Modelling','Architectural, structural and MEP model authoring and documentation',10),
 ('mep_bim','MEP BIM','Mechanical, electrical, plumbing and fire protection modelling',20),
 ('bim_coordination','BIM Coordination','Federated models, clash detection and coordination reporting',30),
 ('bim_training','BIM Training','Individual, corporate and team training programmes',40),
 ('bim_consulting','BIM Consulting','Standards, ISO 19650 readiness and implementation guidance',50),
 ('bim_company_support','BIM Company Support','Overflow production and white-label support for BIM companies',60),
 ('resource_support','Staff / Resource Support','Dedicated modellers, coordinators and teams',70),
 ('engineering_support','Engineering Support','Documentation and technical production support',80),
 ('automation','Software / Automation','Revit automation, data extraction and custom workflows',90),
 ('general','General Enquiry','Uncategorised business enquiries',100),
 ('partnership','Partnership','Partner, vendor and collaboration enquiries',110),
 ('careers','Careers','Job applications and internships',120)
on conflict (code) do nothing;

insert into crm.services (category_id, code, name, sort_order)
select c.id, s.code, s.name, s.sort
from (values
 ('bim_modelling','arch_bim','Architectural BIM',10),
 ('bim_modelling','struct_bim','Structural BIM',20),
 ('bim_modelling','revit_modelling','Revit Modelling',30),
 ('bim_modelling','bim_conversion','CAD to BIM Conversion',40),
 ('bim_modelling','model_updating','Model Updating',50),
 ('bim_modelling','asbuilt_bim','As-Built BIM',60),
 ('bim_modelling','bim_documentation','BIM Documentation',70),
 ('mep_bim','hvac','HVAC Modelling',10),
 ('mep_bim','electrical','Electrical Modelling',20),
 ('mep_bim','plumbing','Plumbing & Public Health',30),
 ('mep_bim','fire_protection','Fire Protection',40),
 ('mep_bim','mep_coordination','MEP Coordination',50),
 ('mep_bim','mep_documentation','MEP Documentation',60),
 ('bim_coordination','clash_detection','Clash Detection',10),
 ('bim_coordination','federated_models','Federated Models',20),
 ('bim_coordination','coordination_reports','Coordination Reports',30),
 ('bim_coordination','issue_management','Issue Management',40),
 ('bim_training','revit_arch','Revit Architecture Training',10),
 ('bim_training','revit_struct','Revit Structure Training',20),
 ('bim_training','revit_mep','Revit MEP Training',30),
 ('bim_training','navisworks','Navisworks Training',40),
 ('bim_training','acc_docflow','ACC & Document Workflow Training',50),
 ('bim_training','bim_fundamentals','BIM Fundamentals',60),
 ('bim_training','corporate_training','Corporate / Team Training',70),
 ('bim_consulting','iso19650_prep','ISO 19650 Readiness',10),
 ('bim_consulting','standards_setup','Standards & Templates Setup',20),
 ('bim_consulting','bim_implementation','BIM Implementation',30),
 ('bim_consulting','cert_guidance','Certification Guidance',40),
 ('bim_company_support','overflow_production','Overflow Production',10),
 ('bim_company_support','white_label','White-label Production',20),
 ('bim_company_support','qaqc_support','QA/QC Support',30),
 ('bim_company_support','process_setup','Process & Template Setup',40),
 ('resource_support','bim_modeler','BIM Modeller',10),
 ('resource_support','revit_mep_modeler','Revit MEP Modeller',20),
 ('resource_support','bim_coordinator','BIM Coordinator',30),
 ('resource_support','dedicated_team','Dedicated BIM Team',40),
 ('automation','revit_automation','Revit Automation',10),
 ('automation','data_extraction','Model Data Extraction',20),
 ('automation','custom_workflows','Custom Workflows',30)
) as s(cat, code, name, sort)
join crm.service_categories c on c.code = s.cat
on conflict (code) do nothing;

insert into crm.lost_reasons (code, name) values
 ('price','Price / budget mismatch'),('timeline','Timeline could not be met'),
 ('capability','Outside current capability'),('no_response','No response from prospect'),
 ('competitor','Awarded to another supplier'),('cancelled','Project cancelled or postponed'),
 ('unqualified','Not a genuine opportunity'),('other','Other')
on conflict (code) do nothing;

-- ------------------------------------------------------- scoring rules ----
-- Tune these in the CRM settings screen; no code change is required.
insert into crm.lead_scoring_rules (code, label, points, field, operator, value, sort_order) values
 ('business_email','Business email domain (not a free provider)',10,'email','matches',
   '^[^@]+@(?!gmail\.|yahoo\.|outlook\.|hotmail\.|live\.|icloud\.|aol\.|proton)',10),
 ('has_company','Company name supplied',10,'company_name','present',null,20),
 ('has_phone','Telephone supplied',5,'phone','present',null,30),
 ('has_project_info','Project type supplied',10,'project_type','present',null,40),
 ('clear_service','Service requirement stated',15,'service_interest','present',null,50),
 ('has_deadline','Required delivery date supplied',10,'required_delivery_date','present',null,60),
 ('has_budget','Budget indicated',10,'estimated_budget','present',null,70),
 ('multi_discipline','Multiple disciplines involved',10,'disciplines','present',null,80),
 ('mep_project','MEP or BIM project type',15,'lead_type','in','mep_bim,bim_modelling,bim_coordination',90),
 ('company_support','BIM company support enquiry (recurring revenue)',15,'lead_type','eq','bim_company_support',95),
 ('international','International commercial enquiry',15,'is_international','eq','true',100),
 ('enterprise','Enterprise-sized company',10,'company_size','in','201-1000,1000+',110),
 ('detailed_message','Detailed requirement text',10,'message','matches','.{200,}',120),
 ('student','Individual or student enquiry',-10,'company_size','eq','individual',200),
 ('careers','Careers enquiry, not a sales lead',-15,'lead_type','eq','careers',210),
 ('vague','Very short or unclear requirement',-15,'message','matches','^.{0,40}$',220),
 ('no_company','No company supplied',-10,'company_name','absent',null,230)
on conflict (code) do nothing;

-- ------------------------------------------------------- routing rules ----
-- assign_to_user is intentionally NULL: routing targets a ROLE and the engine
-- picks the least-loaded active holder, so no person's name is hard-coded.
insert into crm.lead_routing_rules
 (code, label, priority, match_lead_type, match_international, match_min_score,
  assign_to_role, set_priority) values
 ('hot_international','International lead scoring 76+ to senior BD',10,null,true,76,
   'business_development','urgent'),
 ('company_support','BIM company support to business development',20,'bim_company_support',null,null,
   'business_development','high'),
 ('mep_bim','MEP BIM enquiries to the BIM manager queue',30,'mep_bim',null,null,'bim_manager','high'),
 ('bim_modelling','BIM modelling enquiries to sales',40,'bim_modelling',null,null,'sales','normal'),
 ('coordination','Coordination enquiries to the BIM manager queue',50,'bim_coordination',null,null,
   'bim_manager','normal'),
 ('training','Training enquiries to sales',60,'bim_training',null,null,'sales','normal'),
 ('consulting','Consulting and certification to business development',70,'bim_consulting',null,null,
   'business_development','normal'),
 ('resource','Resource and staffing requests to business development',80,'resource_support',null,null,
   'business_development','normal'),
 ('careers','Careers enquiries to admin',90,'careers',null,null,'admin','low'),
 ('fallback','Everything else to the general sales queue',999,null,null,null,'sales','normal')
on conflict (code) do nothing;

insert into crm.app_settings (key, value, description) values
 ('acknowledgement_enabled','true'::jsonb,'Send an acknowledgement email to the enquirer'),
 ('internal_notify_enabled','true'::jsonb,'Notify the internal team on new qualified leads'),
 ('notify_min_score','21'::jsonb,'Minimum lead score that triggers an internal notification'),
 ('response_sla_hours','48'::jsonb,'Published response commitment, in working hours'),
 ('upload_max_bytes','52428800'::jsonb,'Maximum single upload size in bytes'),
 ('upload_allowed_mime',
  '["application/pdf","image/png","image/jpeg","application/zip","application/acad","image/vnd.dwg","model/ifc","application/octet-stream"]'::jsonb,
  'Permitted MIME types for enquiry attachments')
on conflict (key) do nothing;
