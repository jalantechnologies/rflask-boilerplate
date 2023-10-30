describe('Login', () => {
  let credentials;

  beforeEach(() => {
    cy.task('scenario:setup', 'login').then((creds) => {
      credentials = creds;
    });
    cy.visit('/');
  });

  it('loads the login component', () => {
    cy.get('form').should('be.visible');
  });

  it('should allow login', () => {
    cy.get('#username').clear();
    cy.get('#username').type(credentials.username);
    cy.get('#password').clear();
    cy.get('#password').type(credentials.password);
    cy.get('button').click();

    cy.get('#success').should('be.visible').should('have.text', 'SUCCESS!');
  });

  it('should not allow login for removed credentials', () => {
    cy.task('scenario:cleanup', 'login');
    cy.get('#username').clear();
    cy.get('#username').type(credentials.username);
    cy.get('#password').clear();
    cy.get('#password').type(credentials.password);
    cy.get('button').click();

    cy.get('#error').should('be.visible').should('have.text', 'ERROR!');
  });

  afterEach(() => {
    credentials = null;
    cy.task('scenario:cleanup', 'login');
  });
});
