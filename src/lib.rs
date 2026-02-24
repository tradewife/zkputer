pub mod adapters;
pub mod engine;
pub mod models;
pub mod policy;
pub mod prover;
pub mod templates;
pub mod verifier;

pub use engine::ReceiptEngine;
pub use models::{
    ClaimType, NonProvableReason, ProofRequest, ReceiptStatus, Venue, ZKReceipt,
};
pub use prover::{
    build_mvp_prover, FallbackProver, PicoMvpProver, ProverBackend, ProverStrategy, Sp1MvpProver,
};
pub use templates::{
    build_request_from_template, list_verification_templates, template_ids,
    TEMPLATE_ORDER_PLACEMENT_VERIFICATION, TEMPLATE_TRADE_EXECUTION_VERIFICATION,
};
