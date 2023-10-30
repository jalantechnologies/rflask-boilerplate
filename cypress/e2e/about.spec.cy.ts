describe('About', () => {
  beforeEach(() => {
    cy.visit('/about');
  });

  it('should show company logo on page visit', () => {
    cy.get('#companyLogo').should('be.visible');
  });
});
